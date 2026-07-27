# 1. Site Assessment — Inputs & Capacity Derivation

[← Back to index](../README.md)

**Required inputs from any enquiry:**
- Available roof/land area (sqft)
- Roof type: RCC flat / metal sheet / ground
- Sanctioned load or contract demand (kVA)
- Average monthly consumption (units/kWh) and current tariff category
- Shading obstructions (water tanks, adjacent structures, chimneys)
- Location (city/state) — determines PSH and regulatory regime

**Capacity derivation logic:**
```
Usable area = Site area × (1 − shading/layout loss%)
Feasible capacity (kWp) = Usable area ÷ Area-per-kWp factor
```
- Area-per-kWp factor: 90–110 sqft/kWp (default 100)
- Typical shading/layout loss: 5–12%
- Cross-check against sanctioned load — capacity is often capped by DISCOM connection limits, not just roof area

**Generation formula:**
```
Annual generation (units) = Capacity(kWp) × PSH × 365 × PR
CUF (%) = Generation ÷ (Capacity × 8760) × 100
```
- PSH (Peak Sun Hours, kWh/m²/day) by region:
  - Rajasthan/Jodhpur belt: 5.6–5.8
  - Gujarat/Ahmedabad: 5.5–5.6
  - Chennai/Tamil Nadu: 5.3–5.4
  - Bengaluru/Karnataka: 5.2–5.3
  - Delhi NCR: 5.0–5.2
  - Mumbai/Pune (coastal/monsoon): 4.8–5.0
  - Dubai/UAE: 5.5–5.9 (high, but check thermal derate — see [§3 Financial Model](./03-financial-model.md) and [§2 Product/Spec Selection](./02-product-spec-selection.md))
- PR benchmark: 75% (below-average install) / 80% (standard good EPC) / 85%+ (premium, well-monitored)
- Degradation: 2–2.5% year-1 dip, then 0.4–0.5%/year for silicon; HJT trends toward the lower end (~0.3–0.4%/yr)
