# Accacia — Solar EPC Knowledge Bank

A reference base for **C&I rooftop solar** site analysis, product selection, and deal
structuring, focused on the **100 kW – 1.5 MW / ₹50L–5Cr** segment (India-first, with a
GCC/Dubai layer).

## Contents

Each section lives in its own file under [`sections/`](./sections) for quick tool-lookup.

| § | Section | What it covers |
|---|---|---|
| 1 | [Site Assessment](./sections/01-site-assessment.md) | Required enquiry inputs, capacity derivation, generation/CUF formulas, PSH by region |
| 2 | [Product/Spec Selection](./sections/02-product-spec-selection.md) | Cell-technology decision matrix (PERC/TOPCon/HJT/IBC), default-quote rule, physics-to-spec cheat sheet |
| 3 | [Financial Model](./sections/03-financial-model.md) | CAPEX / RESCO formula bank, LCOE·IRR·NPV, India 2026 assumption ranges |
| 4 | [Regulatory & Commercial](./sections/04-regulatory-commercial.md) | Grid-connection mechanisms, CAPEX-vs-RESCO selector, PPA clauses, India + GCC compliance stacks |
| 5 | [Certification & Differentiation](./sections/05-certification-tiers.md) | Tier 1–3 certifications, PVEL 2026 standing of Indian manufacturers |
| 6 | [BOQ Structure](./sections/06-boq-template.md) | 200 kW reference bill-of-quantities template and cost split |
| 7 | [Physics Reference](./sections/07-physics-reference.md) | The "why" behind the specs (p-n junction, bandgap, recombination, PID) |
| 8 | [Terminology Index](./sections/08-terminology-index.md) | Quick-lookup glossary of acronyms and terms |

## Quoting engine

The knowledge bank isn't just reference text — most of it is encoded into a
working **enquiry-to-quote tool**, the `accacia` Python package (pure standard
library, tested). It turns the KB's "required inputs from any enquiry" into a
capacity derivation (§1), a spec recommendation (§2), a full CAPEX/RESCO
financial model (§3 — payback, LCOE, IRR, NPV), a bill of quantities (§6), plus
structuring (§4) and vendor-shortlisting (§5) helpers.

```bash
python -m accacia --area 20000 --location Ahmedabad --load 250 \
    --climate hot --payback-focused --boq
```

Prefer a UI? Open **[`web/index.html`](./web/index.html)** in a browser — a
self-contained page that mirrors the same logic, no install required.

See **[docs/quoting-engine.md](./docs/quoting-engine.md)** for the CLI reference,
library API, and modelling notes.

## Scope & intent

This is a working reference for scoping enquiries, selecting product/spec tiers, building
financial models, and structuring deals — not a substitute for site-specific engineering or
current regulatory verification. Figures reflect **India, 2026** market conditions; always
verify tariffs, ALMM/DISCOM rules, and equipment listings at point of procurement.
