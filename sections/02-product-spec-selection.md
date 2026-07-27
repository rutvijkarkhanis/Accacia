# 2. Product/Spec Selection Logic — Cell Technology Decision Matrix

[← Back to index](../README.md)

| Site condition | Recommended tech | Why |
|---|---|---|
| Standard flush rooftop, moderate climate, budget-sensitive | **Mono PERC / TOPCon (monofacial, glass-backsheet)** | Best ₹/W, mature supply chain, adequate for most C&I deals |
| Hot climate (Rajasthan, Gujarat, Dubai/GCC), high roof temps | **HJT** or **TOPCon with strong temp coefficient datasheet** | Lower %/°C loss protects generation in high ambient heat |
| Elevated/ground-mount with reflective surface (white gravel, light roofing) | **Bifacial TOPCon or HJT, glass-glass** | Captures rear-side reflected light; flush monofacial roofs waste this |
| Roof space is the binding constraint (small footprint, high load) | **HJT, IBC, or BC-hybrid** | Maximizes watts/sqft when area, not budget, is the limiter |
| Aesthetic-sensitive (visible facade, premium commercial, BIPV) | **IBC / Back Contact (BC)** | No front gridlines — uniform black surface; bifaciality loss is irrelevant on flush/facade mounting |
| Long-hold asset (client keeps plant 20–25 yrs, cares about lifetime yield over sticker price) | **HJT** | Lower degradation compounds significantly by year 15–25 |
| Standard 5–8 year payback-focused C&I buyer | **TOPCon** | Best balance of cost, efficiency, bankability, and available financing comfort in 2026 |
| Cool/moderate climate, modest sun exposure (e.g., Punjab, hilly regions) | **TOPCon over HJT** | HJT's heat/temp advantage doesn't materialize; premium doesn't pay back |

**Cross-cutting default rule:** if the buyer hasn't stated a clear priority, quote **Mono TOPCon, half-cut cells, glass-backsheet, monofacial, PVEL Top Performer BOM** as the base case, and offer HJT/bifacial as a clearly priced upgrade tier — this mirrors how the market itself has converged (TOPCon ~60-66% global share in 2026).

**Physics-to-spec cheat sheet (why each spec matters):**
- Higher PVEL designation count / IEC 61215:2021 edition (includes MQT21 PID test) → lower long-term degradation risk
- Half-cut cells → better partial-shading tolerance (independent of cell technology)
- Glass-glass construction → mandatory for bifacial, better moisture resistance, heavier/costlier
- DC:AC ratio 1.1–1.3x → captures more energy across the day without wasting inverter capacity
- ALMM listing (exact model, not brand) → mandatory for subsidy/govt-linked projects in India

> See also: [Section 5 Certification & Differentiation Tiers](./05-certification-tiers.md) for PVEL/BOM detail, and [Section 7 Physics Reference](./07-physics-reference.md) for the underlying mechanisms.
