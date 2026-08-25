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

---

## `deadline_type`

| Value | Meaning |
|-------|---------|
| `consultation_close` | Responses due to the regulator. |
| `compliance_date` | Obligation bites; firms must be compliant. |
| `application_date` | Instrument applies, possibly with transitional relief. |
| `transposition` | EU only — member states must have implemented. |
| `reporting_date` | A submission or return falls due. |
| `expiry` | A licence, exemption or general licence lapses. |

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

**EU** — `EC`, `EBA`, `ESMA`, `EIOPA`, `ECB`, `AMLA`, `EDPB`
**UK** — `FCA`, `PRA`, `BoE`, `HMT`, `OFSI`, `NCA`, `ICO`, `PSR`
**US** — `FinCEN`, `OFAC`, `OCC`, `CFPB`, `FRB`, `FDIC`, `SEC`, `CFTC`, `NYDFS`, `DOJ`
