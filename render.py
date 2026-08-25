#!/usr/bin/env python3
"""
Render the RegWatch register into published artefacts.

    python3 render.py                 # render everything
    python3 render.py --week 2026-08-24
    python3 render.py --check         # validate only, write nothing

Outputs:
    briefs/regwatch-<week>.md   one brief per register file
    DEADLINES.md                rolling calendar across all weeks
"""

from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

import yaml

from site_page import render_index

ROOT = Path(__file__).parent
REGISTER = ROOT / "register"
BRIEFS = ROOT / "briefs"

HORIZON_DAYS = 60

REQUIRED = [
    "id", "jurisdiction", "regulator", "regulator_short", "instrument_type",
    "title", "published", "source_url", "entity_scope", "functions_affected",
    "scores", "rationale", "required_action", "status",
]

JURISDICTIONS = {"EU", "UK", "US"}


# ---------------------------------------------------------------- scoring

def materiality(item: dict) -> float:
    s = item["scores"]
    return round(s["actionability"] * 0.6 + s["reach"] * 0.4, 2)


def band(score: float) -> str:
    if score >= 4.0:
        return "High"
    if score >= 2.5:
        return "Medium"
    return "Low"


# ------------------------------------------------------------- validation

def validate(item: dict, path: Path, errors: list[str]) -> None:
    ref = item.get("id", "<no id>")

    for field in REQUIRED:
        if item.get(field) in (None, "", []):
            errors.append(f"{path.name}:{ref} missing required field '{field}'")

    if item.get("jurisdiction") not in JURISDICTIONS:
        errors.append(f"{path.name}:{ref} jurisdiction must be one of {JURISDICTIONS}")

    url = str(item.get("source_url", ""))
    if not url.startswith("https://"):
        errors.append(f"{path.name}:{ref} source_url must be an https primary source")

    for axis in ("actionability", "reach"):
        v = (item.get("scores") or {}).get(axis)
        if not isinstance(v, int) or not 1 <= v <= 5:
            errors.append(f"{path.name}:{ref} scores.{axis} must be an integer 1-5")

    if item.get("deadline") and not item.get("deadline_type"):
        errors.append(f"{path.name}:{ref} has a deadline but no deadline_type")

    if "verified" not in item:
        errors.append(f"{path.name}:{ref} missing 'verified' (use null if unchecked)")


def load() -> tuple[list[tuple[Path, dict]], list[str]]:
    weeks, errors = [], []
    for path in sorted(REGISTER.glob("*.yaml")):
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as exc:
            errors.append(f"{path.name} is not valid YAML: {exc}")
            continue
        for item in data.get("items") or []:
            validate(item, path, errors)
        weeks.append((path, data))
    return weeks, errors


# ---------------------------------------------------------------- render

def fmt_list(values: list[str]) -> str:
    return ", ".join(v.replace("_", " ") for v in values)


def render_brief(week: str, data: dict) -> str:
    items = sorted(data.get("items") or [], key=materiality, reverse=True)
    window = data.get("window") or {}

    out = [
        f"# RegWatch — week ending {week}",
        "",
        f"Window: {window.get('start', '?')} to {window.get('end', '?')}  ",
        f"Items recorded: {len(items)}",
        "",
    ]

    if window.get("coverage") == "partial":
        out += [f"> **Partial window.** {str(window.get('note', '')).strip()}", ""]

    unverified = [i for i in items if not i.get("verified")]
    if unverified:
        out += [
            f"> {len(unverified)} of {len(items)} records have not had their "
            "primary source re-checked. Marked below.",
            "",
        ]

    covered = {i["jurisdiction"] for i in items}
    if missing := JURISDICTIONS - covered:
        out += [f"> No items recorded this week for: {', '.join(sorted(missing))}.", ""]

    out += ["---", ""]

    for item in items:
        score = materiality(item)
        out += [
            f"## {item['title']}",
            "",
            f"**{item['regulator_short']} · {item['jurisdiction']} · "
            f"{item['instrument_type'].replace('_', ' ')}**"
            + (f" · {item['reference']}" if item.get("reference") else ""),
            "",
            f"Materiality: **{band(score)}** ({score}) · "
            f"actionability {item['scores']['actionability']}/5 · "
            f"reach {item['scores']['reach']}/5",
            "",
            f"Published {item['published']}"
            + (f" · effective {item['effective']}" if item.get("effective") else "")
            + (f" · {str(item.get('deadline_type', 'deadline')).replace('_', ' ')} "
               f"{item['deadline']}" if item.get("deadline") else ""),
            "",
            f"*Who it catches:* {fmt_list(item['entity_scope'])}  ",
            f"*Whose desk:* {fmt_list(item['functions_affected'])}",
            "",
            str(item["rationale"]).strip(),
            "",
            f"**Action:** {str(item['required_action']).strip()}",
            "",
            f"Source: <{item['source_url']}>"
            + (f" · re-checked {item['verified']}" if item.get("verified")
               else " · **source not re-checked**"),
            "",
            "---",
            "",
        ]

    out += [
        "Maintained from primary sources. Not legal advice — see `rubric.md`",
        "for method and limitations.",
        "",
    ]
    return "\n".join(out)


def render_deadlines(weeks: list[tuple[Path, dict]]) -> str:
    today = dt.date.today()
    horizon = today + dt.timedelta(days=HORIZON_DAYS)

    rows = []
    for _, data in weeks:
        for item in data.get("items") or []:
            if item.get("status") != "open":
                continue
            for date_field, kind in (
                (item.get("deadline"), item.get("deadline_type") or "deadline"),
                (item.get("effective"), "compliance_date"),
            ):
                if isinstance(date_field, dt.date) and today <= date_field <= horizon:
                    rows.append((date_field, kind, item))

    rows.sort(key=lambda r: (r[0], -materiality(r[2])))

    out = [
        "# Deadlines",
        "",
        f"Open items falling due in the next {HORIZON_DAYS} days, "
        f"as at {today.isoformat()}.",
        "",
    ]

    if not rows:
        out += ["Nothing falling due in the window.", ""]
        return "\n".join(out)

    out += [
        "| Date | Days | Jur. | Regulator | What | Type | Materiality |",
        "|------|------|------|-----------|------|------|-------------|",
    ]
    for date_field, kind, item in rows:
        days = (date_field - today).days
        title = item["title"] if len(item["title"]) <= 60 else item["title"][:57] + "..."
        out.append(
            f"| {date_field.isoformat()} | {days} | {item['jurisdiction']} "
            f"| {item['regulator_short']} | [{title}]({item['source_url']}) "
            f"| {kind.replace('_', ' ')} | {band(materiality(item))} |"
        )
    out.append("")
    return "\n".join(out)


# ------------------------------------------------------------------ main

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--week", help="render one week only, e.g. 2026-08-24")
    ap.add_argument("--check", action="store_true", help="validate only")
    args = ap.parse_args()

    weeks, errors = load()

    if errors:
        print(f"{len(errors)} validation error(s):", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    if not weeks:
        print("No register files found.", file=sys.stderr)
        return 1

    if args.check:
        items = [i for _, d in weeks for i in (d.get("items") or [])]
        unver = sum(1 for i in items if not i.get("verified"))
        print(f"OK — {len(weeks)} week(s), {len(items)} item(s), no errors.")
        if unver:
            print(f"note: {unver} item(s) awaiting source re-check.")
        return 0

    BRIEFS.mkdir(exist_ok=True)
    for path, data in weeks:
        week = path.stem
        if args.week and week != args.week:
            continue
        target = BRIEFS / f"regwatch-{week}.md"
        target.write_text(render_brief(week, data), encoding="utf-8")
        print(f"wrote {target.relative_to(ROOT)}")

    (ROOT / "DEADLINES.md").write_text(render_deadlines(weeks), encoding="utf-8")
    print("wrote DEADLINES.md")

    (ROOT / "index.html").write_text(render_index(weeks, materiality), encoding="utf-8")
    print("wrote index.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
