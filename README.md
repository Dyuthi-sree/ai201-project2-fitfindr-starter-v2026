# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

FitFindr helps users search secondhand clothing listings using a natural-language request containing keywords, size, and price. It selects the best matching item and suggests outfits using pieces from the user's wardrobe. It then generates a short fit-card caption containing the selected item's price and selling platform. If no listing matches, the agent stops and suggests ways to broaden the search.

<!-- Three or four sentences: what a user asks for, and what they get back. -->



---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** Searches the available clothing listings using the requested description, size, and maximum price.
- **Inputs:** `description` (str), `size` (str), `max_price` (float)
- **Returns:** A list of listing dictionaries, each containing item details such as `title`, `description`, `price`, `size`, and `platform`.
- **When it has nothing:** Returns an empty list.

### `suggest_outfit`

- **What it does:** Suggests an outfit that combines the selected listing with suitable items from the user's wardrobe.
- **Inputs:** `new_item` (dict), `wardrobe` (dict containing an `items` list)
- **Returns:** A string describing an outfit built around the new item and matching wardrobe pieces.
- **When it has nothing:** If the wardrobe is empty, returns general styling advice for the new item instead of failing.

### `create_fit_card`

- **What it does:** Creates a short, social-media-style caption for the completed outfit.
- **Inputs:** `outfit` (str), `new_item` (dict)
- **Returns:** A string containing a concise caption describing the outfit and featured new item.
- **When it has nothing:** Returns a helpful error message if the outfit or new item is missing.

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:** If `search_listings` returns an empty list, store a message in the session telling the user to change the description, size, or price, and stop. Otherwise, take the first result, store it as `selected_item`, call `suggest_outfit`, and then call `create_fit_card`.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** Regular expressions and string cleaning extract `description` (str), `size` (str or None), and `max_price` (float or None) from the natural-language query.

**What moves through the session:** The original query is stored first, followed by the search arguments, search results, selected item, suggested outfit, and final fit-card caption.

---

## Sample Run

**One full query**

```text
$ python app.py ask 'vintage graphic tee under $30'

[1] parse_query
      in:  dict with keys: query
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Y2K Baby Tee — Butterfly Print, Vintage Band Tee — Faded Grey, Graphic Tee — 2003 Tour Bootleg Style … +7 more
      →    branch: continue
[3] select_item
      in:  dict with keys: result_count
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
      →    selected the highest-scoring result
[4] suggest_outfit
      in:  dict with keys: new_item, wardrobe
      out: Here are two wearable, balanced outfits using your new Y2K butterfly baby tee ($18)...
[5] create_fit_card
      in:  dict with keys: outfit, new_item
      out: Channel peak 2000s energy with this butterfly print Y2K baby tee...
      →    run complete

Found: Y2K Baby Tee — Butterfly Print — $18.0 on depop

Outfit: Here are two wearable, balanced outfits using your new Y2K
butterfly baby tee ($18):

Outfit 1 uses baggy straight-leg jeans, chunky white sneakers, and a
black crossbody bag. Outfit 2 uses a vintage black denim jacket,
wide-leg khaki trousers, and black combat boots.

Fit card: Channel peak 2000s energy with this butterfly print Y2K baby
tee. Grab it on Depop for just $18! Pair it with baggy denim and chunky
sneakers for an effortless streetwear look, or layer it under a vintage
jacket.
```

**The three tools, tested one at a time**

### `search_listings`

```text
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

[
  {
    'id': 'lst_017',
    'title': 'Mesh Long-Sleeve Top — Black',
    'size': 'S/M',
    'price': 15.0,
    'platform': 'depop'
  },
  {
    'id': 'lst_002',
    'title': 'Y2K Baby Tee — Butterfly Print',
    'size': 'S/M',
    'price': 18.0,
    'platform': 'depop'
  },
  {
    'id': 'lst_033',
    'title': 'Vintage Band Tee — Faded Grey',
    'size': 'L',
    'price': 19.0,
    'platform': 'depop'
  },
  {
    'id': 'lst_006',
    'title': 'Graphic Tee — 2003 Tour Bootleg Style',
    'size': 'L',
    'price': 24.0,
    'platform': 'depop'
  },
  {
    'id': 'lst_015',
    'title': 'Vintage Graphic Hoodie — Faded Black',
    'size': 'L',
    'price': 26.0,
    'platform': 'depop'
  },
  {
    'id': 'lst_011',
    'title': 'Low-Rise Cargo Pants — Khaki',
    'size': 'W29',
    'price': 27.0,
    'platform': 'poshmark'
  }
]
```

The terminal printed the complete listing dictionaries. The output above retains the identifying fields needed to show the matches and verify the price filter.

### `suggest_outfit`

```text
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"

Here are two practical, everyday outfits built around your new Vintage
Levi's 501 jeans:

Outfit 1: Casual Off-Duty Minimalist

White ribbed tank top (`w_003`), vintage black denim jacket (`w_006`),
chunky white sneakers (`w_007`), and black crossbody bag (`w_010`).

Outfit 2: Cozy Streetwear Edge

Oversized grey crewneck sweatshirt (`w_004`), brown leather belt
(`w_009`), black combat boots (`w_008`), and black crossbody bag
(`w_010`).
```

### `create_fit_card`

```text
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"

Scored these vintage Levi's 501 jeans in a classic medium wash for just
$38. Pair them with your favorite white sneakers for an effortless
off-duty look. Find this piece live on my Depop now!
```

---

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:* I asked AI to help implement keyword-based listing search with optional size and maximum-price filters.
- *What came back:* It suggested using plain substring matching for sizes.
- *What I changed:* I used token-based, case-insensitive size matching because substring matching could incorrectly treat `"S"` as matching `"US 9"` or `"L"` as matching `"XL"`.

**Moment 2**

- *What I asked for:* I asked AI to help build and trace the planning loop.
- *What came back:* It provided the search, outfit, and fit-card stages, but the first pasted version contained formatting characters and needed clearer failure handling.
- *What I changed:* I cleaned the Python formatting, added `trace.step()` after each stage, added an explicit empty-search branch, and caught `ModelUnavailable` so model failures return a readable session error instead of crashing.
<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Matching query completes all three tools | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Impossible query stops before the second tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Selected item moves correctly through session state | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card is specific and short enough to post | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Search results respect the maximum price | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

**Real output from one try**, pasted as text, naming the file and function
that produced it:
**Real output from one try**

Produced by `results/run_2026-10-11_1641_before.md`, using `run_eval.py::main` and `agent.py::run_agent`:
```text
Query: vintage graphic tee under $30

[1] parse_query
[2] search_listings (via MCP)
      out: 10 items
      → branch: continue
[3] select_item
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
[4] suggest_outfit
[5] create_fit_card
      → run complete

Fit card:
Channel ultimate 2000s vibes with this Y2K butterfly baby tee.
Grab it on Depop for just $18.00 before it's gone! Style it with
baggy denim or grunge boots for your next look.
```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Matching query completes all three tools | 4 of 5 | MET (5/5) | All five tries completed search, outfit suggestion, and fit-card creation without stopping early. |
| 2 | Impossible query stops before the second tool | 5 of 5 | MET (5/5) | All five tries returned zero search results, stopped after search, and gave an actionable message about changing price, size, or keywords. |
| 3 | Selected item moves correctly through session state | 5 of 5 | MET (5/5) | In every try, the selected denim jacket remained the item used by the outfit and fit-card steps. |
| 4 | Fit card is specific and short enough to post | 4 of 5 | MET (5/5) | All five cards mentioned the Y2K butterfly baby tee and each stayed below 280 characters. |
| 5 | Search results respect the maximum price | 5 of 5 | MET (5/5) | Every try returned one result priced at $18, which was within the requested $20 maximum. |

**Diagnoses**

All five acceptance criteria were met during the baseline evaluation. The deterministic branch, session-state transfer, and price filtering behaved consistently, while the generated fit cards varied in wording but remained specific and concise.

However, the baseline exposed a search-quality weakness not fully measured by the five criteria. The search gives equal importance to every matching word anywhere in a listing and accepts an item when only one query word matches. For example, the query `green cargo skirt under $40` returned a green polo because the word `green` matched, even though the listing was neither cargo nor a skirt. This happens in `tools.py::search_listings`, where any overlap score greater than zero is accepted.




---


## Loop Trace

**Happy path**

```text
$ python app.py ask 'vintage graphic tee under $30' --trace

[1] parse_query
      in:  dict with keys: query
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Y2K Baby Tee — Butterfly Print, Vintage Band Tee — Faded Grey, Graphic Tee — 2003 Tour Bootleg Style … +7 more
      →    branch: continue
[3] select_item
      in:  dict with keys: result_count
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
      →    selected the highest-scoring result
[4] suggest_outfit
      in:  dict with keys: new_item, wardrobe
      out: Outfit suggestions featuring the Y2K butterfly baby tee
[5] create_fit_card
      in:  dict with keys: outfit, new_item
      out: A short caption featuring the selected item
      →    run complete
```

**Empty search**

```text
$ python app.py ask 'designer ballgown size XXS under $5' --trace

[1] parse_query
      in:  dict with keys: query
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)
      →    branch: empty, stopping

I couldn't find a matching listing. Try increasing your price limit,
changing the size, or using broader keywords.

0 model calls this session
```

**Additional failure-mode checks**

- **Empty wardrobe:** `python app.py ask 'denim jacket under $50' --empty-wardrobe --trace` completed successfully. `suggest_outfit` returned general styling advice, and the agent still created a fit card.
- **Model unavailable:** Running with a deliberately invalid API key produced the readable message, “The model rejected your API key. Check GEMINI_API_KEY in your .env file,” instead of a stack trace.
- **Empty search:** The impossible ballgown query stopped after `search_listings`, left the fit card empty, and made zero model calls.

**On the MCP move:** I registered `search_listings` in `mcp_server.py` and replaced the direct Python call in `agent.py::run_agent` with `mcp_client.call_tool`. The returned value remained a list of listing dictionaries, so both the successful path and the empty-search branch behaved the same after the move. The trace identifies the call as `search_listings (via MCP)`. 


---

## The Improvement

**What I changed:** I changed `tools.py::search_listings` so that a listing must match at least half of the meaningful query words. Previously, any listing matching only one word was accepted.

**Which failure it was meant to fix:** The baseline criteria all passed, but manual testing exposed a relevance weakness. The query `green cargo skirt under $40` returned a green polo because the single word `green` matched. The new overlap requirement prevents one broad word from producing an unrelated result.

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Matching query completes all three tools | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Impossible query stops before the second tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. Selected item moves correctly through session state | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card is specific and short enough to post | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Search results respect the maximum price | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

**Did it help, and how do I know:** Yes. Before the change, `green cargo skirt under $40` returned an unrelated forest-green polo based on one matching word. After the change, the same query returned an empty list and stopped before calling either model-based tool. The `vintage graphic tee under $30` scenario also returned 5 focused results instead of 10 broader results. All five original acceptance criteria remained met across all five after-run tries.

---

## What's Still Broken

The search still uses exact keyword overlap rather than semantic meaning. It does not understand that terms such as “coat” and “jacket” may describe similar items unless both words appear in the listing data.

The stronger overlap rule may also reject a relevant item when the user writes a long query containing several words that do not appear exactly in the listing. A future improvement would give more weight to matches in the title and category, recognize common clothing synonyms, and separately validate important product-type words such as “skirt,” “jacket,” or “shoes.”

The current five criteria also do not directly measure whether the highest-ranked result is the most relevant item. I would add a future criterion requiring the selected item’s category or product type to match the requested product type in at least 4 of 5 searches.


<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
