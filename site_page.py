"""
Landing page generator for the Regulatory Horizon Register.

Imported by render.py. Rebuilds index.html from the register on every run, so
the page is never staler than the register itself.

Three strings to replace before the first commit — see CONTACT below.
"""

from __future__ import annotations

import datetime as dt
import html

# ---------------------------------------------------------------- CONTACT
# REPLACE these three before publishing.
NAME = "Eunice Rosado Almanzar"
LINKEDIN = "https://www.linkedin.com/in/rosadoalmanzar-eunice"
EMAIL = ""  # intentionally not published; contact via LinkedIn
CV_PATH = ""  # no CV published

REPO = "https://github.com/eunicerosado/regulatory-horizon-register"

# The page shows two sections, each capped separately.
#
#   Latest sweep — every record from the most recent window, so the newest work
#                  always reaches the page. Four slots: one reserved for each
#                  jurisdiction that reported, then filled by materiality.
#   Still live   — open records from earlier weeks whose deadline has not yet
#                  passed. Four slots, by materiality.
#
# Before 2026-10-16 the page drew six entries from the whole register with ties
# broken oldest-first, so a new record could only appear by beating an incumbent
# outright. The page was effectively frozen while "last updated" kept moving,
# which is misleading on a site about currency. Ties now break newest-first, and
# an item with no deadline leaves the page once its week is no longer the latest
# — which is the honest behaviour for a horizon register.
LATEST_ENTRIES = 4
STILL_LIVE_ENTRIES = 4

# True = only records whose primary source has been re-checked appear here.
VERIFIED_ONLY = False

CSS = """
:root{
  --paper:#F5F6F7; --ink:#16202B; --muted:#5C6873; --rule:#D6DBDF;
  --link:#1F4E5F; --high:#6B2D3C; --med:#41566A; --low:#686F77;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{
  margin:0; background:var(--paper); color:var(--ink);
  font-family:Newsreader,Georgia,serif; font-size:19px; line-height:1.55;
  padding:0 24px;
}
.wrap{max-width:720px; margin:0 auto; padding:88px 0 72px}
.mono{
  font-family:"IBM Plex Mono",ui-monospace,SFMono-Regular,Menlo,monospace;
  font-size:12px; letter-spacing:.09em; text-transform:uppercase;
}
.eyebrow{color:var(--muted); margin:0 0 28px}
h1{
  font-size:clamp(30px,5.2vw,44px); line-height:1.18; font-weight:400;
  letter-spacing:-.015em; margin:0 0 26px; max-width:17em;
}
.lede{margin:0 0 12px; max-width:34em}
.lede.sub{color:var(--muted); font-size:17px; margin-bottom:40px}
h2{font-size:12px; margin:0 0 14px; font-weight:400; color:var(--muted)}
.entries{border-top:1px solid var(--rule)}
.entry{
  display:block; padding:20px 0; border-bottom:1px solid var(--rule);
  text-decoration:none; color:inherit;
}
.entry:hover .title,.entry:focus-visible .title{color:var(--link)}
.meta{color:var(--muted); display:flex; gap:14px; align-items:center; margin-bottom:7px}
.title{font-size:18px; line-height:1.4; display:block; max-width:40em}
.band{font-weight:500}
.band.high{color:var(--high)} .band.med{color:var(--med)} .band.low{color:var(--low)}
/* signature: two rules whose length encodes actionability and reach */
.gauge{display:inline-flex; flex-direction:column; gap:3px; color:var(--med); margin-left:auto; flex:none}
.gauge .g{display:flex; gap:2px}
.gauge i{display:block; width:6px; height:3px; background:#DFE3E6}
.gauge i.on{background:currentColor}
.unver{color:var(--muted); border:1px solid var(--rule); padding:1px 5px; border-radius:2px}
.due{color:var(--high); font-weight:500}
h2+.entries{margin-bottom:0}
.entries+h2{margin-top:44px}
.gauge.high{color:var(--high)}
.gauge.low{color:var(--low)}
.links{margin:52px 0 0; padding:0; list-style:none; display:flex; flex-wrap:wrap; gap:8px 26px}
.links a{color:var(--link); text-decoration:none; border-bottom:1px solid transparent; padding-bottom:2px}
.links a:hover,.links a:focus-visible{border-bottom-color:var(--link)}
footer{margin-top:64px; padding-top:22px; border-top:1px solid var(--rule); color:var(--muted)}
footer p{margin:0 0 8px; font-size:15px; max-width:38em}
a:focus-visible,.entry:focus-visible{outline:2px solid var(--link); outline-offset:3px}
@media (max-width:560px){
  .wrap{padding:56px 0 48px}
  .meta{flex-wrap:wrap; gap:10px}
  .gauge{margin-left:0}
}
.entry{opacity:0; animation:rise .5s ease forwards; animation-delay:var(--d,0s)}
@keyframes rise{from{opacity:0; transform:translateY(6px)}to{opacity:1; transform:none}}
@media (prefers-reduced-motion:reduce){.entry{opacity:1; animation:none}}
"""


def _band(score: float) -> tuple[str, str]:
    if score >= 4.0:
        return "High", "high"
    if score >= 2.5:
        return "Medium", "med"
    return "Low", "low"


def _as_date(value) -> dt.date | None:
    """Register dates arrive as date objects from YAML, but tolerate strings."""
    if isinstance(value, dt.date):
        return value
    if not value:
        return None
    try:
        return dt.date.fromisoformat(str(value))
    except ValueError:
        return None


def _entry(item, n: int, materiality, due: dt.date | None = None) -> str:
    """One linked row. `due` adds the deadline to the meta line."""
    label, cls = _band(materiality(item))
    act = item["scores"]["actionability"]
    rch = item["scores"]["reach"]
    cells = lambda count: "".join(
        f'<i class="{"on" if k < count else ""}"></i>' for k in range(5)
    )
    flag = "" if item.get("verified") else '<span class="unver">unverified</span>'
    due_cell = f'\n          <span class="due">due {due}</span>' if due else ""

    return f"""      <a class="entry" href="{html.escape(item['source_url'])}"
         style="--d:{0.04 * n:.2f}s" rel="noopener">
        <span class="meta mono">
          <span>{item['published']}</span>
          <span>{html.escape(item['jurisdiction'])} · {html.escape(item['regulator_short'])}</span>
          <span class="band {cls}">{label}</span>{due_cell}
          {flag}
          <span class="gauge {cls}" role="img" aria-label="Actionability {act} of 5, reach {rch} of 5">
            <span class="g">{cells(act)}</span>
            <span class="g">{cells(rch)}</span>
          </span>
        </span>
        <span class="title">{html.escape(' '.join(item['title'].split()))}</span>
      </a>"""


def render_index(weeks, materiality) -> str:
    today = dt.date.today()

    open_items, latest_pool = [], []
    last = max(
        (d["window"]["end"] for _, d in weeks if (d.get("window") or {}).get("end")),
        default=today,
    )
    for _, d in weeks:
        end = (d.get("window") or {}).get("end")
        for item in (d.get("items") or []):
            if item.get("status") != "open":
                continue
            if VERIFIED_ONLY and not item.get("verified"):
                continue
            open_items.append(item)
            if end == last:
                latest_pool.append(item)

    # Materiality first, then newest first. The second term is what stops the
    # page freezing: on a tie the more recent record wins, where it used to lose.
    def rank(item):
        pub = _as_date(item.get("published"))
        return (-materiality(item), -(pub.toordinal() if pub else 0))

    open_items.sort(key=rank)
    latest_pool.sort(key=rank)

    # Reserve one slot for the strongest item in each jurisdiction that reported
    # this week before filling by materiality. The page claims three
    # jurisdictions; it should not then show four items from one.
    latest, seen = [], set()
    for item in latest_pool:
        if item["jurisdiction"] not in seen:
            latest.append(item)
            seen.add(item["jurisdiction"])
    for item in latest_pool:
        if len(latest) >= LATEST_ENTRIES:
            break
        if item not in latest:
            latest.append(item)
    latest.sort(key=rank)
    latest = latest[:LATEST_ENTRIES]

    # Still live: anything not already shown whose deadline is still ahead.
    shown = {id(i) for i in latest}
    still_live = [
        i for i in open_items
        if id(i) not in shown
        and (_as_date(i.get("deadline")) or dt.date.min) >= today
    ][:STILL_LIVE_ENTRIES]

    jurisdictions = sorted({i["jurisdiction"] for i in open_items}) or ["EU", "UK", "US"]

    n = 0
    sections = []
    if latest:
        rows = []
        for item in latest:
            due = _as_date(item.get("deadline"))
            rows.append(_entry(item, n, materiality, due=due if due and due >= today else None))
            n += 1
        sections.append(
            f'  <h2 class="mono">Week ending {last} — highest materiality first</h2>\n'
            f'  <div class="entries">\n{chr(10).join(rows)}\n  </div>'
        )
    if still_live:
        rows = []
        for item in still_live:
            rows.append(_entry(item, n, materiality, due=_as_date(item["deadline"])))
            n += 1
        sections.append(
            '  <h2 class="mono">Still live — earlier records whose deadline has not passed</h2>\n'
            f'  <div class="entries">\n{chr(10).join(rows)}\n  </div>'
        )
    if not sections:
        sections.append(
            '  <h2 class="mono">Nothing currently open</h2>\n'
            '  <p class="lede sub">The register holds no open record with a live '
            'deadline. The full register is linked below.</p>'
        )
    entries_block = "\n\n".join(sections)

    # Optional links are dropped entirely when unset, rather than rendered blank.
    link_items = [
        f'<li><a href="{REPO}">The full register</a></li>',
        f'<li><a href="{REPO}/blob/main/rubric.md">How it is scored</a></li>',
        f'<li><a href="{html.escape(LINKEDIN)}">LinkedIn</a></li>',
    ]
    if CV_PATH:
        link_items.append(f'<li><a href="{html.escape(CV_PATH)}">CV (PDF)</a></li>')
    if EMAIL:
        link_items.append(
            f'<li><a href="mailto:{html.escape(EMAIL)}">{html.escape(EMAIL)}</a></li>'
        )
    links = ("\n" + " " * 4).join(link_items)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(NAME)} — Regulatory Horizon Register</title>
<meta name="description" content="A weekly register of EU, UK and US regulatory
developments, scored on a published materiality rubric and built from primary
sources. Maintained by {html.escape(NAME)}.">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Regulatory Horizon Register">
<meta property="og:url" content="https://eunicerosado.github.io/regulatory-horizon-register/">
<meta property="og:title" content="Regulatory Horizon Register — EU · UK · US">
<meta property="og:description" content="A weekly record of what changed, and what it obliges. Built only from primary sources, scored on a published rubric.">
<meta property="og:image" content="https://eunicerosado.github.io/regulatory-horizon-register/og-card.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Regulatory Horizon Register — EU, UK and US regulatory change, scored on a published rubric.">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Newsreader:opsz,wght@6..72,300;6..72,400;6..72,500&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<div class="wrap">

  <p class="eyebrow mono">Regulatory horizon register · {' · '.join(jurisdictions)}</p>

  <h1>A weekly record of what changed, and what it obliges.</h1>

  <p class="lede">Most regulatory summaries tell you what happened. The question
  a compliance function is paid to answer is which of the week's developments
  deserve a change of plan.</p>

  <p class="lede sub">Maintained by {html.escape(NAME)} — legal and compliance
  practitioner, twenty years in advisory, due diligence and corporate governance
  at a global bank. Built only from primary sources, scored on a published
  rubric, so the judgment can be argued with.</p>

{entries_block}

  <ul class="links">
    {links}
  </ul>

  <footer>
    <p>Each entry links to the regulator's own page. Scores are one
    practitioner's judgment, published so they can be disagreed with — not a
    standard. Not legal advice, and not a compliance control.</p>
    <p class="mono">Register last updated {last}</p>
  </footer>

</div>
</body>
</html>
"""
