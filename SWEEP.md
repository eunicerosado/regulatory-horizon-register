# Weekly sweep

The operating procedure for adding a window to the register. One file
changes each week; everything else is generated from it.

---

## 1. Sweep

Work the Tier 1 list in [`sources.md`](sources.md) for the seven days ending
Sunday. Trade press may point you at a story; the record links to the
regulator's own page, never the alert that mentioned it.

Nothing outside the window, with one exception — a dated obligation falling in
the next 60 days belongs in the record even if published earlier, because that
is what feeds the deadline calendar.

If the sweep was not run properly, say so rather than publishing a thin week as
a full one. Set `coverage: partial` and write a `note`. A register that
silently records only what a weekly brief happened to catch is not a register.

## 2. Record

One file per week, named for the Sunday it ends: `register/2026-08-30.yaml`.
Never edit a past week to add something new — that is what `supersedes` is for.

Item IDs run `<week-ending>-<jurisdiction>-<nnn>`, jurisdiction lowercase,
sequence counted separately per jurisdiction.

```yaml
# RegWatch register — week ending 2026-08-30

window:
  start: 2026-08-24
  end: 2026-08-30
  coverage: full          # full | partial

items:

  - id: 2026-08-30-eu-001
    jurisdiction: EU
    regulator: European Banking Authority
    regulator_short: EBA
    instrument_type: guidelines
    title: >-
      One sentence saying what the regulator did, wrapped
      across lines like this.
    reference: null
    published: 2026-08-26
    effective: null
    deadline: null
    deadline_type: null
    source_url: https://www.eba.europa.eu/...
    verified: 2026-08-30

    entity_scope:
      - credit_institutions
    functions_affected:
      - compliance
      - financial_crime

    scores:
      actionability: 3
      reach: 4

    rationale: >-
      Why it matters, and what is actually new about it.

    required_action: >-
      What an in-scope firm should do — or "Monitor only."

    status: open
    supersedes: null
```

**Use `>-` for every prose field.** A bare `title:` containing a colon breaks
the parse, and colons turn up constantly in regulator headlines.

## 3. Commit

**Add file → Create new file**. Type `register/2026-08-30.yaml` as the
filename — the slash puts it in the folder — paste the week in, commit to
`main`.

The `validate register` workflow fires on that commit. Green means the file
parsed and every record passed. Red means stop and fix before anything else;
see [Red X, and what caused it](#red-x-and-what-caused-it) below.

## 4. Regenerate

The step that is easy to forget. `validate register` only checks — it writes
nothing. The new brief does not exist yet and the deadline calendar still
reflects last week.

**Actions → refresh generated output → Run workflow.** That runs the full
render: writes `briefs/regwatch-2026-08-30.md`, rebuilds `DEADLINES.md`, and
rewrites `index.html` so the site picks up the new items.

It also runs on its own at 06:00 UTC daily, so skipping this only means waiting
until tomorrow — but the site will look a week behind until it runs.

Then check the site: six entries, highest materiality first, at least one per
jurisdiction where something was recorded.

---

## Fields

Required fields must carry a real value — `null` fails the check. Optional
fields must still be *present*, set to `null` when they do not apply.

| Field | Rule | |
|-------|------|--|
| `id` | Unique. Week, jurisdiction, sequence. | required |
| `jurisdiction` | Exactly `EU`, `UK` or `US`. Uppercase. | required |
| `regulator` | Full name, spelled out. | required |
| `regulator_short` | From [`taxonomy.md`](taxonomy.md). | required |
| `instrument_type` | From [`taxonomy.md`](taxonomy.md). | required |
| `title` | Full sentence. Use `>-`. | required |
| `published` | Date on the regulator's page. | required |
| `source_url` | Must start `https://`. Primary source only. | required |
| `entity_scope` | List. At least one value. | required |
| `functions_affected` | List. At least one value. | required |
| `scores` | Both axes, integers 1–5, unquoted. | required |
| `rationale` | The judgment. Use `>-`. | required |
| `required_action` | Or "Monitor only." Use `>-`. | required |
| `status` | `open` or `closed`. | required |
| `verified` | Key must exist. Date re-checked, or `null`. | must be present |
| `reference` | Notice or rule number, if there is one. | optional |
| `effective` | Date the obligation bites. | optional |
| `deadline` | Feeds the 60-day calendar. | optional |
| `deadline_type` | **Mandatory if `deadline` is set.** | optional |
| `supersedes` | `id` of the record this replaces. | optional |

Controlled vocabulary for `instrument_type`, `deadline_type`, `entity_scope`,
`functions_affected` and `regulator_short` lives in
[`taxonomy.md`](taxonomy.md). Add a term there before using it in a record.

## Scoring

Two axes, 1–5, combined `(actionability × 0.6) + (reach × 0.4)`. Full
definitions in [`rubric.md`](rubric.md).

| Score | Actionability | Reach |
|-------|---------------|-------|
| 5 | Binding, dated deadline. Systems or policy must change. | Cross-sector, or a whole major sector. |
| 4 | Binding, but long window or one function. | A defined sector or licence category. |
| 3 | Supervisory expectation. Must evidence a position. | A sub-population — threshold, model, product. |
| 2 | Direction of travel. Planning assumptions move. | Narrow. A handful of firms. |
| 1 | Informational. Enforcement outcome or restatement. | Firm-specific. |

**High** ≥ 4.0 leads the brief and stays in the calendar until closed.
**Medium** 2.5–3.9 is briefed but not chased. **Low** < 2.5 is recorded for
continuity only.

## Red X, and what caused it

| Message | Cause |
|---------|-------|
| `... is not valid YAML` | Indentation, or an unquoted colon — usually a `title:` or `rationale:` written flat instead of with `>-`. Two spaces per level, never tabs. |
| `missing required field 'x'` | Field absent, empty, or `null`. Required fields need a real value. |
| `jurisdiction must be one of {'EU', 'UK', 'US'}` | Lowercase, misspelled, or a fourth jurisdiction. |
| `source_url must be an https primary source` | `http://` rather than `https://`, or the field is empty. |
| `scores.actionability must be an integer 1-5` | Quoted (`'4'`), decimal (`4.5`), or out of range. Bare whole numbers only. |
| `has a deadline but no deadline_type` | A date was set without saying what kind. |
| `missing 'verified' (use null if unchecked)` | The key must be there even when unchecked. `null` is an honest answer; omitting it is not. |

## Continuity

When a development moves, do not rewrite the old record. Write a new one in the
current week, set `supersedes` to the old `id`, and change the old record's
`status` to `closed`. Closed items drop out of the deadline calendar and off
the site but stay in the register — which is what makes it possible to look
back and see what was thought at the time.

A record only earns a new entry if it has *materially* moved. A consultation
closing on schedule with no published outcome is not news.

---

Only `register/` is edited by hand. `briefs/`, `DEADLINES.md` and `index.html`
are generated — editing them directly means losing the change on the next
render.
