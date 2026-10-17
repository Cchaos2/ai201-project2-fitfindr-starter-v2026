"""
The runs your test needs. ← UNIT 4, MILESTONE 3

`run_eval.py` runs every scenario here five times, with the cache off.

How the scenarios map onto my five criteria (criteria.md):

  Criterion 1 (matching query completes, 4 of 5)
      -> scenario "c1/c3/c4 graphic tee", its five tries.
  Criterion 2 (impossible query stops before suggest_outfit, 5 of 5)
      -> scenario "c2 impossible query", its five tries.
  Criterion 3 (item selected == item suggest_outfit received, 5 of 5,
               over five DIFFERENT matching queries)
      -> the five "c3" scenarios. Try k in the run log = query k. A query
         passes only if all five of its repeats pass.
  Criterion 4 (fit card: 2-4 sentences, garment word, $price, platform,
               at least 4 of 5 per item, three items)
      -> the first three scenarios (tee / jacket / dress), five tries each.
         Logged as rows 4a, 4b, 4c. Garment word = the noun in the title.
  Criterion 5 (search respects the price ceiling, 5 of 5)
      -> the five "tee under $N" scenarios. Try k in the run log = N value k.

One run can be scored against more than one criterion: the graphic tee run
is a full three-tool run (criterion 1), it shows the id handed from the
session to suggest_outfit (criterion 3), and it produces a fit card
(criterion 4). The "criterion" key below is the main one; "also" lists the
others. run_eval.py ignores "also"; it is here for the reader.
"""

SCENARIOS = [
    # ── criteria 1, 3, 4 ──────────────────────────────────────────────────
    {
        "name": "c1/c3/c4 graphic tee",
        "query": "vintage graphic tee under $30",      # -> lst_006, tee, $24, depop
        "wardrobe": "example",
        "criterion": 1,
        "also": [3, 4],
        "garment": "tee",
    },
    {
        "name": "c3/c4 denim jacket",
        "query": "denim jacket under $50",             # -> lst_007, jacket, $42, poshmark
        "wardrobe": "example",
        "criterion": 3,
        "also": [4],
        "garment": "jacket",
    },
    {
        "name": "c3/c4 silk slip dress",
        "query": "silk slip dress in midi length under $40",  # -> lst_013, dress, $30, depop
        "wardrobe": "example",
        "criterion": 3,
        "also": [4],
        "garment": "dress",
    },
    {
        "name": "c3 track jacket size M",
        "query": "90s track jacket in size M",         # -> lst_004
        "wardrobe": "example",
        "criterion": 3,
    },
    {
        "name": "c3 corduroy pants",
        "query": "corduroy pants under $35",           # -> lst_005
        "wardrobe": "example",
        "criterion": 3,
    },

    # ── criterion 2 ───────────────────────────────────────────────────────
    {
        "name": "c2 impossible query",
        "query": "designer ballgown size XXS under $5",
        "wardrobe": "example",
        "criterion": 2,
    },

    # ── criterion 5 ───────────────────────────────────────────────────────
    {"name": "c5 tee under $15", "query": "tee under $15", "wardrobe": "example", "criterion": 5, "max_price": 15},
    {"name": "c5 tee under $20", "query": "tee under $20", "wardrobe": "example", "criterion": 5, "max_price": 20},
    {"name": "c5 tee under $25", "query": "tee under $25", "wardrobe": "example", "criterion": 5, "max_price": 25},
    {"name": "c5 tee under $30", "query": "tee under $30", "wardrobe": "example", "criterion": 5, "max_price": 30},
    {"name": "c5 tee under $40", "query": "tee under $40", "wardrobe": "example", "criterion": 5, "max_price": 40},

    # ── diagnostic, not one of the five ───────────────────────────────────
    {
        "name": "empty wardrobe",
        "query": "denim jacket under $50",
        "wardrobe": "empty",
        "criterion": None,
    },
]

WARDROBES = ("example", "empty")


def validate() -> list[str]:
    """Complain about anything malformed, before a long run rather than during."""
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("query", "").strip():
            problems.append(f"scenario {i} has no query")
        if scenario.get("wardrobe") not in WARDROBES:
            problems.append(
                f"scenario {i} has wardrobe {scenario.get('wardrobe')!r} — "
                f"it should be one of {WARDROBES}"
            )
    return problems