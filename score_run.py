"""
Score a run log against my five criteria in criteria.md.   <- UNIT 4, MILESTONE 3

    python score_run.py before        scores results/run_*_before.md
    python score_run.py after         scores results/run_*_after.md

This is test tooling, not part of the agent. It applies the checks written in
criteria.md to the text run_eval.py saved, so every PASS/FAIL comes from the
same rule every time. It reads two files:

  results/run_<stamp>_<label>.md   the report run_eval.py writes
  results/terminal_<label>.txt     the terminal output of that run, saved with
                                   `python -u run_eval.py ... | tee ...`. It
                                   holds the line `suggest_outfit received
                                   id=...` printed INSIDE the tool, which the
                                   report does not keep. Criterion 3 needs it.

It prints one row per criterion in the run-log format, plus the reason for
every FAIL. Spot-check a few against the report by hand.
"""

import re
import sys
from pathlib import Path

import scenarios as scenario_module

RESULTS = Path(__file__).parent / "results"
TRIES = 5


# ── reading the files ─────────────────────────────────────────────────────────

def latest_report(label: str) -> Path:
    found = sorted(RESULTS.glob(f"run_*_{label}.md"))
    if not found:
        sys.exit(f"No results/run_*_{label}.md. Run: python run_eval.py --label {label}")
    return found[-1]


def parse_report(text: str) -> dict:
    """{scenario name: [try dict, ...]} from the report run_eval.py writes."""
    body = text.split("## What actually happened", 1)[-1]
    out = {}
    for section in re.split(r"^### ", body, flags=re.M)[1:]:
        name = section.splitlines()[0].strip()
        tries = []
        for chunk in re.split(r"^\*\*Try \d+\*\*", section, flags=re.M)[1:]:
            t = {"crashed": "Crashed:" in chunk}
            m = re.search(r"^- stopped early: (.*)$", chunk, re.M)
            t["stopped"] = bool(m) and m.group(1).startswith("yes")
            t["error"] = m.group(1)[6:] if t["stopped"] else ""
            m = re.search(r"^- search_results: (\d+)", chunk, re.M)
            t["n_results"] = int(m.group(1)) if m else None
            m = re.search(r"Fit card:\s*```\n(.*?)\n```", chunk, re.S)
            t["fit_card"] = m.group(1).strip() if m else ""
            m = re.search(r"Trace:\s*```\n(.*?)\n```", chunk, re.S)
            t["trace"] = m.group(1) if m else ""
            m = re.search(r"prices=\[([^\]]*)\]", t["trace"])
            t["prices"] = [float(p) for p in m.group(1).split(",") if p.strip()] if m else None
            tries.append(t)
        out[name] = tries
    return out


def parse_terminal(text: str) -> dict:
    """{scenario name: [(selected_id, received_id), ...]} from the saved terminal output."""
    names = {s["name"] for s in scenario_module.SCENARIOS}
    out, current, buffer = {}, None, []
    for line in text.splitlines():
        head = re.match(r"^(.*)  \((example|empty) wardrobe\)$", line)
        if head and head.group(1) in names:
            current, buffer = head.group(1), []
            out[current] = []
            continue
        if current is None:
            continue
        if re.match(r"^  try \d+:", line):
            joined = "\n".join(buffer)
            sel = re.search(r"selected id=(\S+)", joined)
            rec = re.search(r"suggest_outfit received id=(\S+)", joined)
            out[current].append((sel and sel.group(1), rec and rec.group(1)))
            buffer = []
        else:
            buffer.append(line)
    return out


# ── the checks, one per criterion ─────────────────────────────────────────────

def check_c1(t):
    if t["crashed"]:
        return False, "crashed"
    if t["stopped"]:
        return False, f"stopped early: {t['error'][:70]}"
    if not t["fit_card"] or t["fit_card"].startswith("No fit card"):
        return False, f"no fit card ({t['fit_card'][:40]!r})"
    return True, ""


def check_c2(t):
    if t["crashed"]:
        return False, "crashed"
    if not t["stopped"]:
        return False, "did not stop"
    if re.search(r"^\[\d+\] suggest_outfit", t["trace"], re.M):
        return False, "suggest_outfit ran (it has a step in the trace)"
    if "You could" not in t["error"]:
        return False, "message does not say what to change"
    return True, ""


def check_c3(pair):
    selected, received = pair
    if not selected or not received:
        return False, f"missing id (selected={selected}, received={received})"
    if selected != received:
        return False, f"selected {selected} but suggest_outfit received {received}"
    return True, ""


def count_sentences(text: str) -> int:
    ends = re.findall(r"[.!?]+(?=\s|$)", text)
    tail = re.split(r"[.!?]+(?=\s|$)", text)[-1]
    return len(ends) + (1 if re.search(r"[A-Za-z]", tail) else 0)


def check_c4(t, garment, price, platform):
    ok, why = check_c1(t)
    if not ok:
        return False, why
    card, problems = t["fit_card"], []
    n = count_sentences(card)
    if not 2 <= n <= 4:
        problems.append(f"{n} sentences")
    if not re.search(rf"\b{garment}s?\b", card, re.I):
        problems.append(f"no '{garment}'")
    if not re.search(rf"\${int(price)}(?!\d)", card):
        problems.append(f"no '${int(price)}'")
    if platform.lower() not in card.lower():
        problems.append(f"no '{platform}'")
    return (not problems), ", ".join(problems)


def check_c5(t, ceiling):
    if t["crashed"]:
        return False, "crashed"
    if not t["n_results"] or not t["prices"]:
        return False, "search returned nothing"
    if max(t["prices"]) > ceiling:
        return False, f"max price {max(t['prices'])} > {ceiling}"
    return True, ""


# ── output ────────────────────────────────────────────────────────────────────

def cell(ok):
    return "PASS" if ok else "FAIL"


def row(label, target, results, need):
    passes = sum(ok for ok, _ in results)
    verdict = f"{'MET' if passes >= need else 'MISSED'} ({passes}/{len(results)})"
    cells = " | ".join(cell(ok) for ok, _ in results)
    return f"| {label} | {target} | {cells} | {verdict} |", passes >= need


def main():
    label = sys.argv[1] if len(sys.argv) > 1 else "before"
    report_path = latest_report(label)
    terminal_path = RESULTS / f"terminal_{label}.txt"
    report = parse_report(report_path.read_text(encoding="utf-8"))
    terminal = parse_terminal(terminal_path.read_text(encoding="utf-8")) if terminal_path.exists() else {}

    from utils.data_loader import load_listings
    from agent import _parse_query
    from tools import search_listings

    by_crit = {}
    for s in scenario_module.SCENARIOS:
        for c in [s.get("criterion")] + s.get("also", []):
            if c:
                by_crit.setdefault(c, []).append(s)

    lines, notes = [], []

    # 1
    s = by_crit[1][0]
    r = [check_c1(t) for t in report[s["name"]]]
    lines.append(row("1. A matching query completes all three tools", "4 of 5", r, 4)[0])
    notes += [f"C1 try {i}: {why}" for i, (ok, why) in enumerate(r, 1) if not ok]

    # 2
    s = by_crit[2][0]
    r = [check_c2(t) for t in report[s["name"]]]
    lines.append(row("2. An impossible query stops before the second tool", "5 of 5", r, 5)[0])
    notes += [f"C2 try {i}: {why}" for i, (ok, why) in enumerate(r, 1) if not ok]

    # 3 — try k = query k; a query passes only if all its repeats pass
    r = []
    if not terminal:
        notes.append(f"C3: {terminal_path.name} not found, cannot score criterion 3")
    for k, s in enumerate(by_crit[3], 1):
        pairs = terminal.get(s["name"], [])
        reps = [check_c3(p) for p in pairs]
        ok = len(reps) == TRIES and all(o for o, _ in reps)
        ids = sorted({p[0] for p in pairs if p[0]})
        r.append((ok, ""))
        notes.append(f"C3 query {k} '{s['query']}': {sum(o for o, _ in reps)}/{len(reps)} repeats matched, ids {ids}")
        notes += [f"   repeat {i}: {why}" for i, (o, why) in enumerate(reps, 1) if not o]
    lines.append(row("3. The item found is the item passed on (try k = query k)", "5 of 5", r, 5)[0])

    # 4 — one sub-row per item
    met_all = True
    for letter, s in zip("abc", [x for x in by_crit[4] if x.get("garment")]):
        item = search_listings(**_parse_query(s["query"]))[0]
        r = [check_c4(t, s["garment"], item["price"], item["platform"]) for t in report[s["name"]]]
        text, met = row(
            f"4{letter}. Fit card facts + length — {s['garment']} (${int(item['price'])}, {item['platform']})",
            "4 of 5", r, 4)
        met_all &= met
        lines.append(text)
        notes += [f"C4{letter} try {i}: {why}" for i, (ok, why) in enumerate(r, 1) if not ok]
    notes.append(f"Criterion 4 overall: {'MET' if met_all else 'MISSED'} (needs all of 4a, 4b, 4c at 4 of 5)")

    # 5 — try k = ceiling k; a ceiling passes only if all its repeats pass
    r = []
    for k, s in enumerate(by_crit[5], 1):
        reps = [check_c5(t, s["max_price"]) for t in report[s["name"]]]
        ok = len(reps) == TRIES and all(o for o, _ in reps)
        r.append((ok, ""))
        prices = report[s["name"]][0]["prices"]
        notes.append(f"C5 ${s['max_price']}: {sum(o for o, _ in reps)}/{len(reps)} repeats ok, returned prices {prices}")
        notes += [f"   repeat {i}: {why}" for i, (o, why) in enumerate(reps, 1) if not o]
    lines.append(row("5. The search respects a price ceiling (try k = $15/$20/$25/$30/$40)", "5 of 5", r, 5)[0])

    print(f"Scored {report_path.name}" + (f" + {terminal_path.name}" if terminal else ""))
    print()
    print("| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |")
    print("|---|---|---|---|---|---|---|---|")
    print("\n".join(lines))
    print("\nDetails:")
    print("\n".join("  " + n for n in notes))


if __name__ == "__main__":
    main()