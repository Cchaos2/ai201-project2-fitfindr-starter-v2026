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

### Unit 4

**Moment 3**

- *What I asked for:* I asked Claude how to check criterion 3 (the item found
  is the item passed on) using the trace I had just added.
- *What came back:* It pointed out that the `new_item=` value in my
  `suggest_outfit` trace step is read from the same `session["selected_item"]`
  it would be compared against, so the check would compare a value with
  itself and could never fail. The real evidence is the
  `suggest_outfit received id=` line printed inside the tool, but
  `run_eval.py` does not save stdout.
- *What I changed:* I ran the eval as
  `python -u run_eval.py ... | tee results/terminal_before.txt` so the tool's
  own print is saved next to the trace, and scored criterion 3 from that file.

**Moment 4**

- *What I asked for:* I asked Claude to turn my five criteria into a scorer
  (`score_run.py`) so 60 runs would be marked PASS/FAIL by the same rules
  every time.
- *What came back:* The first version marked all five criterion 2 tries as
  FAIL. The check looked for the text "suggest_outfit" anywhere in the trace,
  and my own branch note says "stopping before suggest_outfit".
- *What I changed:* The check now looks only for a trace step that starts
  with `[n] suggest_outfit`. Criterion 2 then scored 5/5, which matches the
  trace. I spot-checked other rows by hand against the report, including the
  one criterion 4 FAIL.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

`python -u run_eval.py --label before 2>&1 | tee results/terminal_before.txt`,
scored with `python score_run.py before`. Cache off, temperature 0.9.
Evidence: `results/run_2026-10-17_1810_before.md` (written by
`run_eval.py::main`) and `results/terminal_before.txt`.

How the rows map to tries:
- **1, 2:** one query, Try k = repeat k.
- **3:** five different matching queries, Try k = query k (graphic tee, denim
  jacket, silk slip dress, track jacket size M, corduroy pants). Each ran five
  times and passes only if all five match.
- **4:** three items, five tries each, as rows 4a/4b/4c. A try passes if the
  fit card has 2–4 sentences, the garment word from the title, `$` + the
  whole-dollar price, and the platform. Criterion 4 is met only if all three
  rows reach 4 of 5.
- **5:** Try k = ceiling k ($15, $20, $25, $30, $40). Each ran five times and
  passes only if every returned price is at or under the ceiling.

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. A matching query completes all three tools | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. An impossible query stops before the second tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. The item found is the item passed on | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4a. Fit card facts + length — tee ($24, depop) | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4b. Fit card facts + length — jacket ($42, poshmark) | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4c. Fit card facts + length — dress ($30, depop) | 4 of 5 | PASS | FAIL | PASS | PASS | PASS | MET (4/5) |
| 5. The search respects a price ceiling | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

**Real output — criteria 1, 3 and 5, scenario `c1/c3/c4 graphic tee`, try 1**
(trace from `agent.py::run_agent`; step 2 is `mcp_server.py::search_listings`
via `mcp_client.call_tool`; the `received id` line is printed by
`tools.py::suggest_outfit`; step 5 is `tools.py::create_fit_card`):

```
[1] parse_query (regex)
      in:  vintage graphic tee under $30
      out: description='vintage graphic tee', size=None, max_price=30.0
[2] search_listings (via MCP)
      in:  description='vintage graphic tee', size=None, max_price=30.0
      out: 10 items: Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey, Y2K Baby Tee — Butterfly Print … +7 more
      →    branch: 10 results, continuing; prices=[24.0, 19.0, 18.0, 26.0, 20.0, 15.0, 18.0, 25.0, 22.0, 27.0]
[3] select_item
      in:  search_results[0]
      out: Graphic Tee — 2003 Tour Bootleg Style ($24.0, depop)
      →    selected id=lst_006
suggest_outfit received id=lst_006
[4] suggest_outfit
      in:  new_item=lst_006, wardrobe=10 items
      out: Outfit 1: Pair the graphic tee with the baggy dark-wash jeans, brown leather belt, and black combat boots for …
[5] create_fit_card
      in:  new_item=lst_006, outfit='Outfit 1: Pair the graphic tee with the baggy dark-wash jean'
      out: Scored this 2003 tour bootleg style graphic tee for just $24 on depop and the fit is unreal. It’s in seriously…
[6] done
      →    all three tools ran, returning the session
```

**Real output — criterion 2, scenario `c2 impossible query`, try 1**
(branch in `agent.py::run_agent`, message from `agent.py::_empty_message`):

```
[1] parse_query (regex)
      in:  designer ballgown size XXS under $5
      out: description='designer ballgown', size='XXS', max_price=5.0
[2] search_listings (via MCP)
      in:  description='designer ballgown', size='XXS', max_price=5.0
      out: [] (empty)
      →    branch: empty, stopping before suggest_outfit
stopped early: Nothing matched 'designer ballgown' (size XXS, under $5). You could remove the size, or raise the price limit, or use different words.
```

**Real output — criterion 4, the one FAIL (row 4c, try 2)**, from
`tools.py::create_fit_card`:

```
Found this gorgeous 90s floral silk midi on depop and I'm obsessed. It was only $30 and the condition is great. Can't wait to layer it over a white tank for daytime or throw an oversized crewneck over it when it gets chilly!
```
Has `$30` and `depop`, but no "dress": the card calls it a "90s floral silk
midi", so the garment-word check fails.

---

## Verdicts and Diagnoses

Verdicts are read against the targets in `criteria.md` (written in unit 3,
before any results), using the counts in Run Log — Before. No criteria were
revised: all five could be measured as written.

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | A matching query completes all three tools | 4 of 5 | MET (5/5) | All 5 tries of "vintage graphic tee under $30" ended at the `done` step with a non-empty fit card. 5 ≥ 4. |
| 2 | An impossible query stops before the second tool | 5 of 5 | MET (5/5) | All 5 tries stopped after step 2 with `[] (empty)`, had no `suggest_outfit` step in the trace, and the message says what to change ("You could remove the size, or raise the price limit…"). |
| 3 | The item found is the item passed on | 5 of 5 | MET (5/5) | For each of the 5 queries, in all 5 repeats, `selected id=` in the trace equalled `suggest_outfit received id=` printed inside the tool (lst_006, lst_007, lst_013, lst_004, lst_005). |
| 4 | The fit card has the facts and is caption-length | 4 of 5 per item | MET (4a 5/5, 4b 5/5, 4c 4/5) | Each of the three items reached at least 4 of 5. The tee and the jacket passed every try; the dress failed try 2 on the garment word. |
| 5 | The search respects a price ceiling | 5 of 5 | MET (5/5) | For all five ceilings, every returned price (logged as `prices=[...]` in the trace) was at or under N, in all 5 repeats. Highest returned vs ceiling: 15/$15, 19/$20, 24/$25, 27/$30, 27/$40. |

**Arguing the opposite verdict on criterion 4.** Someone could say the 4c
card ("90s floral silk midi") obviously describes the dress, so try 2 should
count as a PASS and 4c is really 5/5. I kept it as a FAIL: the check was
fixed before the run as "contains the garment word", and "midi" is not
"dress". Either way the verdict is MET. Someone could also argue the other
way: that 14 passes out of 15 is not "4 of 5". But the criterion says "per
item", and each item was scored on its own five tries.

**Diagnoses**

No criterion was missed. There is one individual FAIL, and it is worth
explaining because it is where criterion 4 nearly missed.

*Row 4c, try 2 — place: the model's output in `tools.py::create_fit_card`.*
The card said "Found this gorgeous 90s floral silk midi on depop…" and never
used the word "dress". The prompt sends the full title as
`Item: 90s Silk Slip Dress — Floral, Midi Length`. The system prompt only says
"Mention the item… exactly once", and does not say which word has to survive.
The model shortened the title and kept the descriptors ("90s", "floral",
"silk") plus "midi" from the part after the dash, which it used as the noun
instead of "dress". The tee and jacket titles put the garment word in their
short first part ("Graphic Tee — …", "Denim Jacket — …"), so it survived every
paraphrase. "Dress" sits in a longer title next to another word that can act
as a noun ("Midi"), so it was the one that got dropped. The tool, the search
and the session all worked; the prompt leaves the garment type up to the
model's paraphrase.

*Pattern.* Across all 60 runs, the only failure was in model output. The
three criteria with no model in them (2, 3, 5) passed every try, and
`generate.py` absorbed the two rate-limit pushbacks with retries, so none of
the 55 runs that reached the model crashed or came back empty. Every bit of
variation lives in the two model-calling tools, and the deterministic parts
never varied.

**Which target was set too low, and the tighter one**

*Criterion 1 was set too low.* I allowed one miss in five because a model call
could fail, hit the rate limit or come back empty. In the run that never
happened: 5 of 5 here, and all 55 runs that reached the model completed. The
rate limit was hit twice, and `generate.py` waited and retried both times,
so a pushback slows a run down but does not fail it. The risk I reserved the
miss for is already handled one layer down. Tighter target:
**"Given each of five different matching queries, the agent completes all
three tools and returns a fit card in 5 of 5 tries per query (25 of 25)."**

*Criterion 5's target was at the maximum, but its condition was too easy.*
It only tested one phrasing ("tee under $N"), and every ceiling had at least
one tee under it, so the test could never reach the empty branch or the
other price phrasings `_parse_query` claims to handle. Tighter version:
**"For 'tee under $N', 'tee below $N', 'tee max $N' and 'tee $N' with
N = 15, 20, 25, 30, 40, every returned price is ≤ N in 5 of 5 tries; and
'tee under $10' returns no listings and stops before suggest_outfit, 5 of 5."**

*Criterion 4 was not too low.* It is the one target that actually bit: 4c
landed exactly on the 4 of 5 line. Raising it to 5 of 5 would turn this run
into a miss, so the fix belongs in the prompt (Milestone 5), not in the target.

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

- Registered `search_listings` in `mcp_server.py` with `@mcp.tool()`, typed
  inputs (`description: str`, `size: str | None`, `max_price: float | None`)
  and a description that states units (USD) and the empty case (`[]`).
- Swapped the direct call in `agent.py::run_agent` for
  `call_tool("search_listings", {...})`.
- Removed `search_listings` from the `tools` import, so nothing calls it directly.
- Nothing behaved differently: the list returned over MCP was identical to the
  direct call (`True`), the empty case still came back as `[]` (not `None`),
  and the agent still selected lst_006. The only visible change is a short
  delay, because each call starts the server process.


---

## The Improvement

**What I changed:** one prompt, in `tools.py::create_fit_card`. The code now
pulls the garment word out of the short part of the title (the words before
"—", last word: "Graphic Tee" → `tee`, "Denim Jacket" → `jacket`,
"90s Silk Slip Dress" → `dress`) and sends it to the model as its own line,
`Garment word: dress`. The system prompt gained one rule: "Always name the
item with the exact garment word given (for example 'tee', 'jacket',
'dress'), even when you shorten the title." Nothing else changed: same search,
loop, session, scenarios and scorer.

**Which failure it was meant to fix:** row 4c, try 2 in Run Log — Before. The
card called the dress a "90s floral silk midi" and never said "dress". The
diagnosis was that the old prompt sent only the full title and said "Mention
the item", so when the model shortened a long title it picked the noun
itself, and "Midi" from after the dash replaced "Dress". The fix takes that
choice away from the model.

### Run Log — After

`python -u run_eval.py --label after 2>&1 | tee results/terminal_after.txt`,
scored with `python score_run.py after`. Same scenarios, same scorer, cache
off. 114 model calls, no crashes. Evidence:
`results/run_2026-10-17_1920_after.md` and `results/terminal_after.txt`. Rows
map to tries the same way as in Run Log — Before.

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. A matching query completes all three tools | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. An impossible query stops before the second tool | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. The item found is the item passed on | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4a. Fit card facts + length — tee ($24, depop) | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4b. Fit card facts + length — jacket ($42, poshmark) | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4c. Fit card facts + length — dress ($30, depop) | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. The search respects a price ceiling | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

**Real output — row 4c, try 4 after the change** (`tools.py::create_fit_card`):

```
Score this gorgeous floral midi dress for just $30 on depop. I love styling it with an oversized crewneck and combat boots for that perfect 90s grunge look. It's in great condition and ready for your next weekend outfit.
```

Before the change the model wrote "floral silk midi" with no garment noun.
After it, it writes "floral midi dress": "midi" is still there, but now as an
adjective in front of the garment word.

**Did it help, and how do I know:**
Yes, for the failure it targeted, as far
as five tries can show. Row 4c went from 4/5 to 5/5: all five dress cards in
the after-run contain "dress" ("90s silk slip dress", "floral dress",
"floral midi dress"…), where before one in five did not. Rows 4a and 4b stayed
at 5/5, so the new rule did not push out the price or platform or make the
cards longer than four sentences, and rows 1, 2, 3 and 5 were unchanged. Two
limits on that claim: the before-run had only one FAIL, and five tries cannot
separate an item that keeps the garment word 95% of the time from one that
keeps it 100% of the time, so this shows the observed failure did not repeat,
not that it can't. And one side effect the criteria don't check: in try 2 the
model pasted the full title word for word ("90s Silk Slip Dress — Floral, Midi
Length"), which reads more like a listing than a post. The explicit garment
line may have nudged it toward copying the title instead of paraphrasing it.



---

## What's Still Broken

No criterion is still missed: all five were met before and after the change.
But my tests didn't cover everything, and I found two problems.

**1. Shoe sizes don't match.** Searching "platform sneakers size 8" finds
nothing, even though there is a pair in size "US 8". The search treats "8"
and "US 8" as different sizes, then wrongly tells the user to remove the
size. *What I'd do:* make the search ignore the "US" part when comparing
sizes.

**2. My fix sometimes makes the caption copy the title.** After the change,
one dress caption repeated the full listing title word for word, so it read
more like a product listing than a real post. My criteria don't check for
this. *What I'd do:* add a check that the caption doesn't repeat the full
title, and adjust the prompt. 



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