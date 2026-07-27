# Accacia Quoting Engine

The `accacia` Python package turns a C&I rooftop solar **enquiry into a quote** —
a spec recommendation plus a full financial model — by encoding the logic from
the [Solar EPC Knowledge Bank](../README.md):

| Module | Knowledge Bank section | What it computes |
|---|---|---|
| `accacia.site` | [Section 1 Site Assessment](../sections/01-site-assessment.md) | Usable area → feasible capacity (roof-area vs sanctioned-load bound), year-1 generation, CUF |
| `accacia.specs` | [Section 2 Product/Spec Selection](../sections/02-product-spec-selection.md) | Cell-technology decision matrix as a priority-ordered rule engine |
| `accacia.finance` | [Section 3 Financial Model](../sections/03-financial-model.md) | CAPEX & RESCO year-by-year models, payback, LCOE, IRR, NPV |
| `accacia.regulatory` | [Section 4 Regulatory & Commercial](../sections/04-regulatory-commercial.md) | Grid-connection selector, CAPEX-vs-RESCO selector, PPA clauses, India/GCC compliance checklists |
| `accacia.boq` | [Section 6 BOQ Structure](../sections/06-boq-template.md) | 9-line bill of quantities: cost split, module/inverter counts, per-line specs |
| `accacia.vendors` | [Section 5 Certification & Differentiation](../sections/05-certification-tiers.md) | PVEL 2026 vendor shortlisting and ranking |
| `accacia.quote` | — | Orchestrates site/spec/finance/BOQ into one `Quote` |

A browser front-end that mirrors this logic (no install, no CLI) lives at
[`web/index.html`](../web/index.html) — open it directly in a browser.

## Install / run

No third-party runtime dependencies (pure standard library). Run straight from
the repo:

```bash
python -m accacia --area 20000 --location Ahmedabad --load 250 \
    --climate hot --payback-focused --schedule
```

Or install it (adds an `accacia` console command and enables tests):

```bash
pip install -e ".[test]"
accacia --area 20000 --psh 5.55 --json
pytest
```

## CLI

| Flag | Maps to | Default |
|---|---|---|
| `--area` (required) | Section 1 roof/land area (sqft) | — |
| `--location` / `--psh` | Section 1 PSH (region lookup or explicit) | one required |
| `--pr` | Section 1 performance ratio | 0.80 (good-EPC benchmark) |
| `--load` | Section 1 sanctioned load (kVA) — DISCOM capacity cross-check | none |
| `--shading-loss`, `--area-per-kwp`, `--capacity` | Section 1 overrides | 0.08, 100, — |
| `--climate {hot,moderate,cool}` and spec flags | Section 2 decision matrix | moderate |
| `--cost-per-watt`, `--grid-tariff`, `--tariff-escalation`, `--tenure`, `--discount-rate` | Section 3 assumptions | India-2026 midpoints |
| `--module-wp`, `--inverter-kw`, `--dc-ac-ratio` | Section 6 BOQ sizing | 580 Wp, 100 kW, 1.2 |
| `--json`, `--schedule`, `--boq` | output format | text summary |

Spec flags: `--reflective-mount`, `--space-constrained`, `--aesthetic`,
`--long-hold`, `--payback-focused`, `--budget-sensitive`. They resolve in the
priority order of the Section 2 matrix (a physical constraint outranks a climate match,
which outranks a cost preference); with none set, the KB base-case rule fires.

## Library

```python
from accacia import Enquiry, build_quote
from accacia.specs import SiteConditions

quote = build_quote(Enquiry(
    site_area_sqft=20000,
    location="Ahmedabad",
    sanctioned_load_kva=250,
    conditions=SiteConditions(climate="hot", payback_focused=True),
))
print(quote.summary())
quote.to_dict()   # JSON-serialisable full quote incl. year-by-year rows
```

### Section 4 structuring & Section 5 vendor helpers

These stand alone from the site→quote pipeline — call them to advise on
structuring and procurement:

```python
from accacia import (
    recommend_grid_connection, recommend_commercial_model,
    compliance_checklist, recommend_vendors,
)

recommend_grid_connection(184).choice                # "Net metering"
recommend_grid_connection(1500).choice               # "Open access" (over state cap)
recommend_commercial_model(has_capital=True, tax_appetite=True,
    wants_zero_upfront=False, can_absorb_performance_risk=True).choice   # "CAPEX / EPC"
compliance_checklist("india")                        # legal-gatekeeper checklist
recommend_vendors(3)                                 # Adani, RenewSys, ReNew (by PVEL standing)
```

## Modelling notes

- **Capacity is the binding minimum** of roof-area capacity and the
  sanctioned-load ceiling (KB: capacity is often capped by DISCOM limits, not
  roof area). `binding_constraint` reports which one bound.
- **Degradation** uses a distinct first-year dip (default 2%) and a lower
  steady-state rate (default 0.5%/yr) rather than one compounding rate, so
  year-1 generation and payback are not overstated.
- **RESCO tariff** is derived as `grid × (1 − discount)` (default 22% discount,
  inside the KB's 20–25% range) and escalates independently.
- **IRR** is solved by bisection on the CAPEX cashflows; it returns `None` only
  when no sign change exists (savings never turn positive), and can legitimately
  be negative when savings never recover capex.
- **BOQ cost allocation** splits total CAPEX across the 9 Section 6 line items by the
  KB cost-split percentages (modules 57.5%, inverters 11%, BOS 16.5%, the six
  remaining lines share the leftover 15%); the line costs always reconcile to
  CAPEX. Module and inverter counts are derived from `--module-wp` and the
  `--dc-ac-ratio` / `--inverter-kw`, and the Section 2 cell-tech recommendation flows
  into the module line's spec text.
- **Defaults** sit at the midpoints of the KB "India, 2026" assumption ranges.
  Override any of them per enquiry — always verify tariffs and ALMM/DISCOM rules
  at point of procurement.
