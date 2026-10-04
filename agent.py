"""
The FitFindr planning loop.

This file makes FitFindr an agent rather than a simple script. It decides
which tool to run next based on what the previous tool returned.
"""

import re

import config
import trace
from generate import ModelUnavailable
from tools import create_fit_card, search_listings, suggest_outfit


# ── Session state ──────────────────────────────────────────────────────────────

def new_session(query: str, wardrobe: dict) -> dict:
    """Create and return a fresh session for one user interaction."""
    return {
        "query": query,
        "parsed": {},
        "search_results": [],
        "selected_item": None,
        "wardrobe": wardrobe,
        "outfit_suggestion": None,
        "fit_card": None,
        "error": None,
    }


# ── Planning loop ──────────────────────────────────────────────────────────────

def run_agent(query: str, wardrobe: dict) -> dict:
    """Run the FitFindr planning loop and return the completed session."""
    session = new_session(query, wardrobe)
    trace.start_trace()

    # Extract a price limit such as "under $30".
    price_match = re.search(
        r"(?:under|below|max(?:imum)?|less than)\s*\$?(\d+(?:\.\d+)?)",
        query,
        re.IGNORECASE,
    )
    max_price = float(price_match.group(1)) if price_match else None

    # Extract a clothing size such as "size M".
    size_match = re.search(
        r"\b(?:size\s*)?(XXS|XS|S|M|L|XL|XXL|XXXL)\b",
        query,
        re.IGNORECASE,
    )
    size = size_match.group(1).upper() if size_match else None

    # Remove price, size, and request phrases from the description.
    description = re.sub(
        r"(?:under|below|max(?:imum)?|less than)\s*\$?\d+(?:\.\d+)?",
        "",
        query,
        flags=re.IGNORECASE,
    )

    description = re.sub(
        r"\bsize\s*(?:XXS|XS|S|M|L|XL|XXL|XXXL)\b",
        "",
        description,
        flags=re.IGNORECASE,
    )

    description = re.sub(
        r"\b(?:looking for|find me|show me|i want|i need)\b",
        "",
        description,
        flags=re.IGNORECASE,
    )

    description = " ".join(description.split()).strip(" ,.-")

    session["parsed"] = {
        "description": description,
        "size": size,
        "max_price": max_price,
    }

    trace.step(
        "parse_query",
        inputs={"query": query},
        returned=session["parsed"],
    )

    stage = "search"
    iteration = 0

    try:
        while True:
            iteration += 1
            trace.check_iterations(iteration)

            if stage == "search":
                results = search_listings(
                    description=session["parsed"]["description"],
                    size=session["parsed"]["size"],
                    max_price=session["parsed"]["max_price"],
                )

                session["search_results"] = results

                trace.step(
                    "search_listings",
                    inputs=session["parsed"],
                    returned=results,
                    note=(
                        "branch: continue"
                        if results
                        else "branch: empty, stopping"
                    ),
                )

                if not results:
                    session["error"] = (
                        "I couldn't find a matching listing. Try increasing "
                        "your price limit, changing the size, or using broader "
                        "keywords."
                    )
                    return session

                session["selected_item"] = results[0]

                trace.step(
                    "select_item",
                    inputs={"result_count": len(results)},
                    returned=session["selected_item"],
                    note="selected the highest-scoring result",
                )

                stage = "suggest_outfit"
                continue

            if stage == "suggest_outfit":
                outfit = suggest_outfit(
                    session["selected_item"],
                    session["wardrobe"],
                )

                session["outfit_suggestion"] = outfit

                trace.step(
                    "suggest_outfit",
                    inputs={
                        "new_item": session["selected_item"],
                        "wardrobe": session["wardrobe"],
                    },
                    returned=outfit,
                )

                stage = "create_fit_card"
                continue

            if stage == "create_fit_card":
                fit_card = create_fit_card(
                    session["outfit_suggestion"],
                    session["selected_item"],
                )

                session["fit_card"] = fit_card

                trace.step(
                    "create_fit_card",
                    inputs={
                        "outfit": session["outfit_suggestion"],
                        "new_item": session["selected_item"],
                    },
                    returned=fit_card,
                    note="run complete",
                )

                return session

    except ModelUnavailable as exc:
        session["error"] = str(exc)

        trace.step(
            "model_unavailable",
            inputs={"stage": stage},
            returned=session["error"],
            note="stopping cleanly instead of crashing",
        )

        return session


# ── Run directly ───────────────────────────────────────────────────────────────

def _show(session: dict) -> None:
    """Print the result of one agent session."""
    if session["error"]:
        print(f"  stopped: {session['error']}")
        print(
            f"  fit_card is {session['fit_card']!r} "
            "— it should still be None here"
        )
        return

    item = session["selected_item"] or {}

    print(
        f"  found:    {item.get('title')} — "
        f"${item.get('price')} on {item.get('platform')}"
    )
    print(f"  outfit:   {session['outfit_suggestion']}")
    print(f"  fit card: {session['fit_card']}")


if __name__ == "__main__":
    from utils.data_loader import get_example_wardrobe

    print("=== A query the data can match ===")
    _show(
        run_agent(
            query="looking for a vintage graphic tee under $30",
            wardrobe=get_example_wardrobe(),
        )
    )

    print("\n=== A query it can't match ===")
    _show(
        run_agent(
            query="designer ballgown size XXS under $5",
            wardrobe=get_example_wardrobe(),
        )
    )

    print(
        "\nThe second query should stop before creating the fit card. "
        "If both paths look the same, the branch is not working."
    )