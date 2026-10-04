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
[2] search_listings
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

**One full query**

```
$ python app.py ask '...'

```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

```

```
$ python -c "from tools import suggest_outfit; ..."

```

```
$ python -c "from tools import create_fit_card; ..."

```

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
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

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
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```

```

**Empty search**

```

```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



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
