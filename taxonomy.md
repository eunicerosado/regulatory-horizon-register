# Taxonomy

Controlled vocabulary for the register. The purpose is to make EU, UK and
US developments comparable in one table when the three systems use
different words for similar things — and to keep the differences visible
where they are real rather than flattening them.

Values are `snake_case`. Add new terms here before using them in a record.

---

## `instrument_type`

| Value | EU | UK | US |
|-------|----|----|----|
| `legislation` | Regulation, Directive | Act, Statutory Instrument | Statute, Public Law |
| `technical_standard` | RTS / ITS | — | — |
| `guidelines` | EBA/ESMA Guidelines | FCA/PRA guidance | Interagency guidance |
| `rule_final` | Delegated Act | Policy Statement (PS) | Final Rule |
| `rule_proposed` | Draft Delegated Act | Consultation Paper (CP) | Notice of Proposed Rulemaking (NPRM) |
| `rule_withdrawn` | Withdrawal of a Commission proposal | Revocation, withdrawn proposal | Withdrawal of proposed rule, Rescission |
| `consultation_paper` | Consultation / Call for Advice | Consultation Paper (CP) | Request for Information / ANPR |
| `supervisory_statement` | Opinion, Q&A | Dear CEO letter, SS, Market Watch | Bulletin, Supervisory Letter, Circular |
| `enforcement` | National authority decision | Final Notice | Consent Order, Civil Money Penalty |
| `advisory` | — | — | FinCEN Advisory, OFAC Guidance |
| `sanctions_action` | Council Regulation amendment | OFSI designation | OFAC SDN update, GL, FAQ |
| `report` | Report, Risk Assessment | Thematic Review, Portfolio Letter | Semiannual Risk Perspective, Study |

**Note on non-equivalence.** A UK *Dear CEO letter* and a US *OCC bulletin*
both sit under `supervisory_statement`, but the first is a targeted
supervisory communication and the second is general guidance to the
regulated population. Where the distinction matters to the obligation, say
so in `rationale` rather than forcing the label.

**`rule_withdrawn`** records a proposed or final rule being withdrawn,
rescinded or revoked. It is a direction-of-travel signal in its own right, and
recording it as `rule_proposed` would misstate that direction.

*Amended 2026-10-13 — `rule_withdrawn` added. `2026-10-12-us-002` is the first
record to use it.*

---

## `deadline_type`

| Value | Meaning |
|-------|---------|
| `consultation_close` | Responses due to the regulator. |
| `compliance_date` | Obligation bites; firms must be compliant. |
| `application_date` | Instrument applies, possibly with transitional relief. |
| `transposition` | EU only — member states must have implemented. |
| `reporting_date` | A periodic submission or return falls due. |
| `submission_due` | A one-off application or submission must be filed by this date. |
| `expiry` | A licence, exemption or general licence lapses. |

**`reporting_date` or `submission_due`.** Both are dates by which a firm must
file something, and before 2026-10-13 both were recorded as `reporting_date`.
They are separated because the consequence of missing them differs: a periodic
return filed late is a reporting breach, whereas a one-off application filed
late can cost the right to carry on the activity. An annual frozen asset review
is `reporting_date`; an authorisation gateway application is `submission_due`.
Neither covers the date an instrument starts to apply — that is
`application_date`, even where the instrument introduces a charge or a duty that
someone must then pay or perform.

*Amended 2026-10-13 — `submission_due` added and `reporting_date` narrowed to
periodic filings. `2026-10-06-uk-001` was moved onto the new value. Records
written before this date recorded one-off application deadlines as
`reporting_date`.*

---

## `entity_scope`

`credit_institutions` · `payment_service_providers` · `e_money_institutions`
· `investment_firms` · `crypto_asset_service_providers` · `money_service_businesses`
· `designated_non_financial_businesses` · `insurers` · `fund_managers`
· `all_regulated_firms`

Use the closest licence category, not a colloquial sector name. If an item
catches an unlicensed population — beneficial ownership registers catching
corporates generally, say — record it and explain the perimeter in
`rationale`. Perimeter questions are usually the interesting part.

---

## `functions_affected`

`compliance` · `financial_crime` · `legal` · `risk` · `operations` ·
`onboarding` · `technology` · `data` · `finance` · `board`

`board` is reserved for items that require a governing-body decision,
attestation or documented oversight — not merely items a board would find
interesting.

---

## `regulator_short`

**EU** — `EC`, `Council`, `EBA`, `ESMA`, `EIOPA`, `ECB`, `AMLA`, `EDPB`
**UK** — `FCA`, `PRA`, `BoE`, `HMT`, `OFSI`, `FCDO`, `NCA`, `ICO`, `PSR`
**US** — `FinCEN`, `OFAC`, `OCC`, `CFPB`, `FRB`, `FDIC`, `SEC`, `CFTC`, `NYDFS`, `DOJ`, `FTC`
