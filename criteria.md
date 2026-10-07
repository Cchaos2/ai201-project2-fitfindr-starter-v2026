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

Given a query that matches at least one listing, the agent completes all three
tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**
<!-- Why 4 of 5 and not 5 of 5? Something about your search, probably —
     "my search is a plain keyword match and some phrasings will miss" is a
     real answer. -->
Two of my three tools call a model. A model call can fail, hit the rate
limit, or come back empty, and then there is no fit card. My search is also a
simple keyword match: "top" does not match "tops", and "W30" does not match a
listing sized "W30 L30". One miss in five allows for this. 
---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**
<!-- Why is 5 of 5 reasonable here when criterion 1 isn't? What's different
     about this path? -->
This path never calls a model. My loop checks in plain Python if the
search list is empty and returns right away, so the same query gives the same
result every time. Any miss is a bug.
---

## 3. The item found is the item passed on

Given five different matching queries, the `id` that `suggest_outfit` received
is the same as `session["selected_item"]["id"]`, in 5 of 5 tries. 
<!--
To check:
`suggest_outfit` prints `suggest_outfit received id=...` when it starts. The
tester compares that id with `session["selected_item"]["id"]` printed at the
end of the run.
-->
<!-- YOU WRITE THIS ONE.

     How would you know that the item your search found is the same item the
     next tool received? Name something countable or observable.

     This is the criterion people find hardest, because state failure doesn't
     look like state failure — it looks like a tool problem. Something that
     compares session["selected_item"] against what actually reached
     suggest_outfit is the shape you're after. -->



**Why this target:**
The item goes from the session into the tool with no model in between, so the
result is the same every time and 5 of 5 is the honest target. I compare `id`
because every listing has a different one.


---

## 4. The fit card has the facts and is caption-length

Given three different items, each run 5 times with the cache off, the fit card
passes all four checks in at least 4 of 5 tries per item:
- it has 2 to 4 sentences;
- it contains the garment word
- it contains the price as `$` plus the whole-dollar amount
- it contains the platform name in any letter case

<!-- YOU WRITE THIS ONE.

     The fit card calls a model, so the same input can produce different words
     each time. That's not a bug — it's the nature of the tool. So what would
     make it acceptable?

     Think about what you'd actually be unhappy to see. A caption that never
     mentions the price? Two different items producing the same opening
     sentence? A card longer than a caption anyone would post? Any of those can
     be turned into a number. -->

**Why this target:**
A model writes the card, so the words change on every run. I can only check
things that need no opinion, and these four come from the `create_fit_card`
docstring. The checks are exact text matches, so a good caption can still
fail: "twenty-four bucks" fails the price check. That is why I allow one miss
in five. The cache must be off, because with it on all five tries return the
same saved text.

---

## 5. The search respects a price ceiling

Given the query "tee under $N" for N = 15, 20, 25, 30 and 40, the search
returns at least one listing and every listing it returns has `price <= N`,
in 5 of 5 tries. The tester prints the price of every returned listing and
compares the highest one with N.

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. Speed, the empty
     wardrobe path, what happens when the model can't be reached, whether the
     search respects a price ceiling — anything, as long as it names a number
     or an observable outcome. -->

**Why this target:**
The price check is a number comparison in Python with no model involved, so
one listing over the limit is a bug and 5 of 5 is fair. I only test the form
"under $N".

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
