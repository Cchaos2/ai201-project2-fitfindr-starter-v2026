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

<!-- Three or four sentences: what a user asks for, and what they get back. -->
FitFindr is an assistant that helps users find second-hand clothes. You can describe what you’re looking for in your 
own words, like “vintage graphic tee under $30,” and you can also add your size if you want. The agent searches 
through 40 listings, finds the one that seems like the best match, suggests a few outfits using clothes you already have,
and writes a short caption for the item. If it can’t find anything that works, it stops and tells you what you could change,
such as removing the size requirement or increasing your budget.


---

**(Findings in Milestone 1)**
- There are 11 fields in a listing: id, title, description, category, style_tags, size, condition, price, colors, brand, platform.
- The brand can be null
- A wardrobe item has 6 fields: id, name, category, colors, style_tags, notes.
- There are queries that the data can not match.

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** Filters the listing by a price ceiling and a size, then ranks by the number of keywords that appears.
- **Inputs:** `description` (str), `size` (str or None), `max_price` (float or None).
- **Returns:** A list of at most 10 listing dicts, best match first. Each listing has id, title, description, category, style_tags, size, condition, price, colors, brand, platform.
- **When it has nothing:** An empty list `[]`.

### `suggest_outfit`

- **What it does:** Asks the model for outfits that combine an item with pieces from the wardrobe of the user.
- **Inputs:** `new_item` (dict), `wardrobe` (dict)
- **Returns:** A string with outfits suggestions 
- **When it has nothing:** If the wardrobe has no items, then it is returned a non-empty string of general styling adivce

### `create_fit_card`

- **What it does:** Asks the model to write a short social media caption about the item and the outfit
- **Inputs:** `outfit` (str), `new_item` (dict)
- **Returns:** A string that mentions the item, its price and its platform.
- **When it has nothing:** If `outfit` is empty, a string saying no fit could be written

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

**Branch rule:** If search_listings returns an empty list, put a message in session["error"] and stop. Otherwise, take
the first result and go to suggest_outfit.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** <!-- regex, string splitting, or asking the model — say which -->

**What moves through the session:** <!-- which fields, in what order -->

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask 'vintage graphic tee under $30'
```
suggest_outfit received id=lst_006

  Found:    Graphic Tee — 2003 Tour Bootleg Style — $24.0 on depop

  Outfit:   Buy it. It fits right into your grunge aesthetic and bridges your existing pieces.

Outfit 1 (Casual Streetwear): Pair the graphic tee with your baggy dark-wash jeans, brown leather belt, and chunky white sneakers. Throw your slightly cropped black denim jacket on top and finish with the black crossbody bag.

Outfit 2 (Edgy Casual): Tuck the tee into your wide-leg khaki trousers, add the black combat boots, and layer your black cropped zip hoodie unzipped over the top.

  Fit card: Found this sick 2003 tour bootleg style graphic tee on depop for just $24 and I'm obsessed. It fits right into your grunge aesthetic and bridges your existing pieces. Can't wait to style this with baggy jeans and combat boots!

0 model calls this session, 2 served from cache


**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
```
[{'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s', 'streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}]

```
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))""
```

suggest_outfit received id=lst_001
Buy them. They fill a great middle ground between your baggy dark jeans and wide-leg khakis. 

Outfit 1 (Casual streetwear): Pair the vintage Levi's 501s with the white ribbed tank top, black cropped zip hoodie, and chunky white sneakers. Add the black crossbody bag.

Outfit 2 (Relaxed classic): Wear the 501s with the oversized grey crewneck sweatshirt, black combat boots, and the brown leather belt to add contrast and define your waist.

```
$ python -c "from tools import create_fit_card; ..."
```

Scored these vintage Levi's 501 jeans in a great medium wash on depop for just $38! They’re in solid condition and fit like an absolute dream. I'm totally planning to style them with a simple white tank top, a black denim jacket, and chunky white sneakers.

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:* I gave Claude the size-matching helper code my professor wrote in class and asked it to check the code against the real listings data.
- *What came back:* It found that `p.strip().upper` was missing its parentheses, which crashes with an AttributeError as soon as a query includes a size. It also showed that a plain keyword count ranked "Y2K Baby Tee" above "Graphic Tee" for the query "vintage graphic tee".
- *What I changed:* I fixed the line to `p.strip().upper()` and added a rule in `search_listings` that counts a keyword in the title twice, so the Graphic Tee is ranked first.

**Moment 2**

- *What I asked for:* I showed Claude my first Tool Inventory entry for `search_listings` and asked what I still had to do.
- *What came back:* It pointed out that my Returns line said "Each listing has id, title, description, etc.", and that a vague return value does not earn the points. 
- *What I changed:* I rewrote the Returns line to list all eleven fields of a listing dict

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

Produced by `agent.py::run_agent`, with one `trace.step()` call per pass of
the loop. `search_listings` runs through MCP (`mcp_client.call_tool` →
`mcp_server.py`), which is why its step is labelled `(via MCP)`.

**Happy path** — `python app.py ask 'vintage graphic tee under $30' --trace`

```
[1] parse_query (regex)
      in:  vintage graphic tee under $30
      out: description='vintage graphic tee', size=None, max_price=30.0
[2] search_listings (via MCP)
      in:  description='vintage graphic tee', size=None, max_price=30.0
      out: 10 items: Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey, Y2K Baby Tee — Butterfly Print … +7 more
      →    branch: 10 results, continuing
[3] select_item
      in:  search_results[0]
      out: Graphic Tee — 2003 Tour Bootleg Style ($24.0, depop)
      →    selected id=lst_006
suggest_outfit received id=lst_006
[4] suggest_outfit
      in:  new_item=lst_006, wardrobe=10 items
      out: Buy it. It fits right into your grunge aesthetic and bridges your existing pieces.   Outfit 1 (Casual Streetwe…
[5] create_fit_card
      in:  new_item=lst_006, outfit='Buy it. It fits right into your grunge aesthetic and bridges'
      out: Found this sick 2003 tour bootleg style graphic tee on depop for just $24 and I'm obsessed. It fits right into…
[6] done
      →    all three tools ran, returning the session
```

**Empty search** `python app.py ask 'designer ballgown size XXS under $5' --trace`

```
[1] parse_query (regex)
      in:  designer ballgown size XXS under $5
      out: description='designer ballgown', size='XXS', max_price=5.0
[2] search_listings (via MCP)
      in:  description='designer ballgown', size='XXS', max_price=5.0
      out: [] (empty)
      →    branch: empty, stopping before suggest_outfit
```

The empty run stops after step 2. The branch in `run_agent` sees `[]` from
`search_listings` and returns before `suggest_outfit` is called, so the trace
is 2 steps instead of 6. Step 3 and step 4 also show the item that was
selected (`lst_006`) is the item `suggest_outfit` received (`lst_006`), which
is what criterion 3 checks.

### Failure modes, triggered on purpose

**1. Empty search** — `python app.py ask 'designer ballgown size XXS under $5'`

```
  Nothing matched 'designer ballgown' (size XXS, under $5). You could remove the size, or raise the price limit, or use different words.

0 model calls this session
```

Already handled by the branch in `agent.py::run_agent` (`_empty_message`). No
change needed: it names the filters it used and what to change, and makes no
model calls.

**2. Empty wardrobe** — `python app.py ask 'denim jacket under $50' --empty-wardrobe`

```
(running with an empty wardrobe)
suggest_outfit received id=lst_007

  Found:    Denim Jacket — Light Wash, Cropped — $42.0 on poshmark

  Outfit:   Pair this vintage cropped denim jacket with a classic white crewneck t-shirt and high-waisted black straight-leg jeans. Finish the look with white leather sneakers or black ankle boots for an effortless, streetwear-inspired outfit that works for casual days. Alternatively, layer it over a plain black ribbed midi dress with canvas sneakers for an easy, balanced mix of casual and feminine.

  Fit card: Found this cropped light wash denim jacket on poshmark and I'm obsessed. It was only $42 and is in such amazing condition. Can't wait to wear it with all my high-waisted jeans this fall!

2 model calls this session, 243 prompt + 123 output tokens
```

Already handled in `tools.py::suggest_outfit`: when `wardrobe["items"]` is
empty it switches to a prompt asking for outfits built from common basics, so
it returns general advice (white tee, black jeans, sneakers) instead of
crashing or returning an empty string.

**3. Model unavailable** — one character of `GEMINI_API_KEY` changed in
`.env`, and a query whose item had never been run, so the answer could not
come from the cache.

Before the handler — `python app.py ask 'corduroy pants under $35'`:

```
suggest_outfit received id=lst_005
1 model calls this session

ModelUnavailable: The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com.
```

The exception escaped `run_agent` and was only caught by the catch-all in
`app.py::main`. The session was thrown away, the message did not say which
step failed or that the search had worked, and under `run_eval.py` the run
would be logged as a crash.

After the handler (`try/except ModelUnavailable` around `suggest_outfit` and
`create_fit_card` in `agent.py::run_agent`) — `python app.py ask 'corduroy pants under $30'`:

```
[1] parse_query (regex)
      in:  corduroy pants under $30
      out: description='corduroy pants', size=None, max_price=30.0
[2] search_listings (via MCP)
      in:  description='corduroy pants', size=None, max_price=30.0
      out: 1 items: Low-Rise Cargo Pants — Khaki
      →    branch: 1 results, continuing
[3] select_item
      in:  search_results[0]
      out: Low-Rise Cargo Pants — Khaki ($27.0, poshmark)
      →    selected id=lst_011
suggest_outfit received id=lst_011
[4] suggest_outfit
      in:  new_item=lst_011, wardrobe=10 items
      out: ModelUnavailable
      →    model unreachable, stopping

  The search worked and found Low-Rise Cargo Pants — Khaki ($27 on poshmark), but suggest_outfit couldn't reach the model, so there is no outfit or fit card. The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com. Then run the same query again.

1 model calls this session
```

The run now stops cleanly at step 4 with `session["error"]` set. The message
says what broke (`suggest_outfit` could not reach the model), keeps what did
work (the item found), and says what to do (check the key, then rerun). I used
`$30` instead of `$35` here so the query had not been cached. Side
observation: with the ceiling at $30 the corduroy pants ($32) were filtered
out and the search returned cargo pants, matching only on the word "pants".


**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->

- Swapped the direct call in run_agent for call_tool("search_listings", {...}).
- Removed search_listings from the tools import, so nothing calls it directly.
- The returned list was identical to the direct call (True).
- The empty case still returns [].


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



# COMMAND 1

python app.py ask 'designer ballgown size XXS under $5'

...
Nothing matched 'designer ballgown' (size XXS, under $5). You could remove the size, or raise the price limit, or use different words.
...

# COMMAND 2

python app.py ask 'denim jacket under $50' --empty-wardrobe

...
(running with an empty wardrobe)
suggest_outfit received id=lst_007

  Found:    Denim Jacket — Light Wash, Cropped — $42.0 on poshmark

  Outfit:   Pair this vintage cropped denim jacket with a classic white crewneck t-shirt and high-waisted black straight-leg jeans. Finish the look with white leather sneakers or black ankle boots for an effortless, streetwear-inspired outfit that works for casual days. Alternatively, layer it over a plain black ribbed midi dress with canvas sneakers for an easy, balanced mix of casual and feminine.

  Fit card: Found this cropped light wash denim jacket on poshmark and I'm obsessed. It was only $42 and is in such amazing condition. Can't wait to wear it with all my high-waisted jeans this fall!

0 model calls this session, 2 served from cache
...

# COMMAND 3

python app.py ask 'corduroy pants under $35'

...
suggest_outfit received id=lst_005
1 model calls this session

ModelUnavailable: The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com.
...