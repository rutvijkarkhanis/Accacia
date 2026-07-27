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
- PSH (Peak Sun Hours, kWh/m²/day) by region — planning midpoints; supersede with site-specific resource data:
  - **High (5.5–5.8)** — arid NW belt:
    - Rajasthan/Jodhpur belt: 5.6–5.8 (Jaisalmer highest ~5.75)
    - Jaipur: ~5.6
    - Gujarat/Ahmedabad/Rajkot: 5.5–5.6 (Surat/Vadodara ~5.5)
  - **Good (5.3–5.5)** — central & Deccan plateau:
    - Madhya Pradesh/Bhopal/Indore: 5.4–5.5
    - Chhattisgarh/Raipur: ~5.4
    - Telangana/Hyderabad: ~5.4
    - Andhra Pradesh/Vijayawada: ~5.4 (Visakhapatnam ~5.35)
    - Vidarbha/Nagpur: ~5.4
    - Chennai/Tamil Nadu/Coimbatore: 5.3–5.4
    - Bengaluru/Karnataka: 5.2–5.3
  - **Moderate (5.0–5.2)** — Indo-Gangetic plains / NCR:
    - Delhi NCR/Noida/Gurgaon/Faridabad: 5.0–5.2
    - Haryana: ~5.1
    - Uttar Pradesh/Lucknow/Kanpur: ~5.05
    - Punjab/Ludhiana/Amritsar: ~5.0 (Chandigarh ~5.05)
    - Bihar/Patna, Odisha/Bhubaneswar: ~5.0
  - **Lower (4.6–5.0)** — humid coasts & monsoon/NE belts:
    - Pune ~5.0, Mumbai ~4.9 (coastal/monsoon)
    - Kerala/Kochi: ~4.95
    - West Bengal/Kolkata: ~4.85
    - Assam/Guwahati (NE, cloudy): ~4.6
  - **GCC**: Dubai/UAE 5.5–5.9, Abu Dhabi ~5.75, Sharjah ~5.7 (high, but check thermal derate — see [Section 3 Financial Model](./03-financial-model.md) and [Section 2 Product/Spec Selection](./02-product-spec-selection.md))
- PR benchmark: 75% (below-average install) / 80% (standard good EPC) / 85%+ (premium, well-monitored)
- Degradation: 2–2.5% year-1 dip, then 0.4–0.5%/year for silicon; HJT trends toward the lower end (~0.3–0.4%/yr)
