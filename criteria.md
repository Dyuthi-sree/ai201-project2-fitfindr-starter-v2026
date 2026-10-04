# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"The agent handles errors"* is an opinion.
*"When search returns nothing, the agent stops before calling the second tool,
in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter one. A reason that says something about your tools, your loop, or the
data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

**Two are written for you. You write three.**

---
## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:** The listing search uses words extracted from natural-language queries, so an unusual phrasing may fail to match the stored description. Four of five allows one phrasing mismatch while still requiring the complete agent workflow to work consistently.

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling `suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:** This branch checks a deterministic empty list rather than relying on model-generated language. Therefore, the agent should stop correctly every time and suggest changing the description, size, or maximum price.

---

## 3. The selected item moves correctly through session state

For 5 of 5 matching queries, `session["selected_item"]` must equal the listing passed as `new_item` to `suggest_outfit`.

**Why this target:** The agent is required to carry information between tools through the session. Because both values are directly observable dictionaries, they should match every time without allowing the user to enter the item again.

---

## 4. The fit card is specific and short enough to post

For at least 4 of 5 matching queries, the generated fit card mentions the selected item and contains no more than 280 characters.

**Why this target:** A useful fit card should clearly relate to the item the user selected and be short enough for a social-media caption. I allow one failure because model-generated wording can vary between runs.

---

## 5. Search results respect the maximum price

For 5 of 5 searches that return results, every returned listing must have a price less than or equal to the `max_price` requested by the user.

**Why this target:** Price is a structured numeric field, so the search tool can check it deterministically. Returning even one item above the user’s budget would make the search unreliable.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
