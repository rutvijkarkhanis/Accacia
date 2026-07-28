# 3. Financial Model — Formula Bank

[← Back to index](../README.md)

**CAPEX total:**
```
Capex = Capacity(kWp) × 1000 × Cost per watt (₹/W)
```

**Year-y generation (with degradation):**
```
Generation_y = Capacity × PSH × 365 × PR × (1 − degradation%)^(y−1)
```

**CAPEX model, year-y savings:**
```
Grid rate_y = Grid tariff × (1 + tariff escalation%)^(y−1)
O&M cost_y = Capex × O&M% × (1 + O&M inflation%)^(y−1)   [O&M inflation default: 5%/yr]
CAPEX savings_y = Generation_y × Grid rate_y − O&M cost_y
Cumulative CAPEX = Σ savings_y − Capex (starts negative)
Payback year = first year cumulative CAPEX ≥ 0
```

**RESCO/PPA model, year-y savings:**
```
RESCO rate_y = RESCO tariff × (1 + RESCO escalation%)^(y−1)
RESCO savings_y = Generation_y × (Grid rate_y − RESCO rate_y)
Cumulative RESCO = Σ savings_y (starts at 0, no capex outlay)
```

**Other key metrics to layer in:**
- **LCOE** = Total lifetime cost ÷ Total lifetime generation (₹/unit) — true cost comparator, model-agnostic
- **IRR** — annualized return rate equating cash inflows/outflows; use when comparing solar against other capital projects
- **NPV** — discount future cashflows at cost of capital; solar can have fast payback but weak NPV if discount rate is high
- **Accelerated depreciation** — only relevant/valuable if client has sufficient taxable profit to absorb the deduction (qualifying question before pitching CAPEX)

**Default assumption ranges (India, 2026):**
- Cost per watt: ₹35–45/W (C&I turnkey)
- Grid tariff: ₹7–10/unit (commercial), escalation 3–5%/yr
- O&M: 0.8–1.2% of capex/yr
- RESCO tariff: typically 20–25% below grid tariff
- RESCO escalation: 2–5%/yr

> Generation inputs (PSH, PR, degradation) come from [Section 1 Site Assessment](./01-site-assessment.md); CAPEX-vs-RESCO fit is decided in [Section 4 Regulatory & Commercial Structuring](./04-regulatory-commercial.md).
