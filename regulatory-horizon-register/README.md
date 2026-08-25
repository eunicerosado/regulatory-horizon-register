# Regulatory Horizon Register

A weekly, scored register of financial-crime and financial-services
regulatory developments across the **EU, UK and US** — maintained from
primary sources, with the materiality judgment published alongside each
item rather than left implicit.

Most regulatory summaries tell you what happened. The harder question, and
the one a compliance function is actually paid to answer, is which of the
week's developments deserve a change of plan. This register records that
judgment on a consistent rubric, week after week, so that it can be
reviewed, argued with, and looked back on.

---

## How to read it

| Path | What it is |
|------|-----------|
| [`DEADLINES.md`](DEADLINES.md) | Rolling 60-day calendar of open obligations and consultation closes. Start here. |
| [`briefs/`](briefs) | The rendered weekly brief. Human-readable output. |
| [`register/`](register) | The register itself — one YAML file per week. The source of truth. |
| [`rubric.md`](rubric.md) | How materiality is scored, and what is deliberately excluded. |
| [`taxonomy.md`](taxonomy.md) | Controlled vocabulary mapping EU / UK / US terminology onto comparable terms. |
| [`sources.md`](sources.md) | The sweep universe and the source discipline applied to it. |

`briefs/` and `DEADLINES.md` are generated. Edit the register, not the
output.

---

## Method

**Cadence.** One sweep per week, window stated explicitly on every brief.

**Primary sources only.** Trade press and law-firm alerts may be used to
notice a development. The record links to the regulator's own page, and no
figure, firm name, deadline or rule reference is stated unless it was seen
there. Where something is unconfirmed, the record says so rather than
estimating.

**Two axes, published.** Each item is scored 1–5 on *actionability* (does a
firm have to change something, and how soon) and *reach* (how much of the
regulated population is caught), combined 60/40 into a materiality band.
Full definitions in [`rubric.md`](rubric.md).

**Perimeter is treated as the interesting question.** Where a development
catches a population that would not expect to be caught, that is recorded
in the item's rationale rather than smoothed over by the entity taxonomy.

**Continuity.** Items are not silently rewritten. Where a development
supersedes an earlier one, the new record cites the old by `id` and the
earlier record is marked closed.

---

## Running it

```bash
pip install pyyaml

python3 render.py --check    # validate the register, write nothing
python3 render.py            # rebuild briefs/ and DEADLINES.md
```

`--check` enforces required fields, jurisdiction values, an https
primary-source link, integer scores in range, a `deadline_type` on any item
carrying a deadline, and the presence of a `verified` field. It runs on every
commit.

**Verification.** Every record carries `verified` — the date its primary
source was last re-checked, or null. Unverified records are marked as such in
the rendered brief rather than quietly presented as confirmed. A week may be
published with unverified records; it may not be published pretending
otherwise.

---

## Scope and limitations

This is a horizon-scanning register maintained by one practitioner from
freely available sources. It is not exhaustive, it is not a compliance
control, and **it is not legal or regulatory advice.** No firm should rely
on it to identify its own obligations. Scores are one practitioner's
judgment, published so that they can be disagreed with — not a standard.

Nothing here derives from any employer's or client's confidential material.
Every item traces to a public primary source, linked in the record.

---

## Maintained by

**Eunice Rosado Almanzar** — legal and compliance practitioner. Twenty
years in advisory, due diligence and corporate governance at a global
bank, covering AML/KYC and sanctions, regulatory change, and supervisory
examinations across US, EMEA and APAC. M.Sc. Legal Studies. CRCMP, CISRCP.
Bilingual EN/ES.

Corrections and disagreements are welcome — open an issue.

---

## The landing page

`render.py` also rebuilds `index.html` from the register, so the page can never
be staler than the records behind it. Publish it either way:

- **Project site** — enable Pages on this repo, source `main` / root. Serves at
  `eunicerosado.github.io/regulatory-horizon-register`.
- **Root site** — copy `index.html` into a repo named `eunicerosado.github.io`.
  Serves at `eunicerosado.github.io`.

Contact details live at the top of `site_page.py` (`LINKEDIN`, `EMAIL`,
`CV_PATH`). `EMAIL` and `CV_PATH` are deliberately empty — their links are
omitted from the page rather than rendered blank. Set either to a non-empty
string to bring the link back.
