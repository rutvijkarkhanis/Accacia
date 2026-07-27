# Solar EPC Knowledge Bank

### Reference base for site analysis, product selection, and deal structuring (C&I rooftop, 100 kW – 1.5 MW / ₹50L–5Cr range)

---

## 1. Site Assessment — Inputs & Capacity Derivation

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
  - Dubai/UAE: 5.5–5.9 (high, but check thermal derate — see §3)
- PR benchmark: 75% (below-average install) / 80% (standard good EPC) / 85%+ (premium, well-monitored)
- Degradation: 2–2.5% year-1 dip, then 0.4–0.5%/year for silicon; HJT trends toward the lower end (~0.3–0.4%/yr)

---

## 2. Product/Spec Selection Logic — Cell Technology Decision Matrix

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

---

## 3. Financial Model — Formula Bank

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

---

## 4. Regulatory & Commercial Structuring Layer

**Grid connection mechanisms — pick based on client profile:**
| Mechanism | When it applies |
|---|---|
| Net metering | Standard C&I rooftop, capacity under state cap (varies, often 500kW–1MW) |
| Open access | Large consumer, roof space insufficient, sourcing from an off-site plant |
| Group captive | Multiple consumers jointly own ≥26% of a plant, seeking open-access tariff benefits |
| Gross metering | Rare now — all generation sold separately from consumption billing |

**Commercial model selector:**
- **CAPEX/EPC** → client has capital + tax appetite (accelerated depreciation), wants 100% of savings after payback, can absorb performance risk
- **RESCO/PPA** → client wants zero upfront cost, de-risks completely, accepts a capped long-term savings ceiling; developer needs strong balance sheet/project finance access

**Key PPA clauses to always check for:**
- Tariff structure (fixed vs escalating)
- Minimum guaranteed generation / PR floor with compensation clause
- Contract tenure (15–25 yrs)
- Termination/buyout clause and lock-in period
- Curtailment risk allocation (who absorbs DISCOM export caps/banking rule changes)
- O&M SLA (uptime %, response time, penalties)

**India-specific compliance checklist:**
- BIS certification (IS 14286 modules / IS 16221 & IS 16169 inverters) — mandatory, legal gatekeeper
- ALMM listing — exact model number, required for subsidy/govt-linked projects; verify at point of procurement, not installation
- MNRE empanelment — per DISCOM/state, doesn't auto-extend across regions
- Structural safety certificate — licensed engineer sign-off, required before mounting
- GST/EPFO/MCA21 compliance clean record — informal but real credibility filter in institutional tenders

**GCC (Dubai/DEWA) equivalent stack:**
- DEWA-certified contractor (Category A/B/C by system size)
- DEWA-approved equipment list
- Shams Dubai net metering pathway via Hab Reeh platform
- Note: each UAE emirate runs its own utility program (DEWA ≠ ADDC ≠ EtihadWE) under a shared federal framework — no single GCC-wide rule

---

## 5. Certification & Differentiation Tiers

**Tier 1 — Legal minimum (table stakes, doesn't differentiate)**
- IEC 61215 + IEC 61730 (global) / BIS IS 14286 (India-mandatory)
- Screens mainly for "infant mortality" failures, not full 25-year life prediction
- 2021 edition added MQT21 (PID test) — ask which edition was used

**Tier 2 — Government/subsidy eligibility**
- ALMM listing (model-specific)
- MNRE empanelment

**Tier 3 — Premium differentiation (voluntary, signals real reliability)**
- PVEL/Kiwa PQP Top Performer status — 8 categories: Thermal Cycling, Damp Heat, Mechanical Stress, Hail Stress, PID, UVID, LID+LETID, PAN Performance
- RETC independent testing
- TÜV Rheinland "All Quality Matters" / Long-Term Sequential testing
- Extended/enhanced test duration (2-3x standard damp heat, 400+ thermal cycles)
- EL (Electroluminescence) imaging at manufacture and post-transit

**Indian manufacturers with strong PVEL 2026 standing (for vendor shortlisting):**
- Adani Solar — 7/8 designations (ASB-M10-144-AAA), highest per-model average (6.5), 7 consecutive years Top Performer
- ReNew — 7/8 designations
- RenewSys — 7/8 designations (DESERV EXTREME), avg 5.75/model
- Waaree — largest roster (23 models), 5th consecutive year Top Performer, avg 3.13/model (breadth over concentration)
- Also on list: Grew Solar, EMMVEE, Goldi Solar, Avaada Electro, Gautam Solar, Rayzon Solar, Vikram Solar, Solex, Tata Power Solar

**Diligence question that actually separates vendors:** not "is it certified" but "which IEC edition, does it include MQT21 (PID), and can you show the exact model's PVEL category breakdown + EL images for this specific batch?"

---

## 6. BOQ Structure Template (200 kW reference scale)

1. **Modules** — Wp rating, cell tech, ALMM status, efficiency %, warranty (product/performance)
2. **Inverters** — kW rating, string count, MPPT channels, DC:AC ratio, warranty
3. **Mounting structure (BOS)** — material/galvanization, tilt angle, wind load standard (IS 875)
4. **DC cabling & protection** — cable spec, combiner boxes, SPD, connectors
5. **AC cabling & protection** — cable spec, ACDB, MCCB, step-up transformer (if HT)
6. **Earthing & lightning protection** — pits (IS 3043), arrestors
7. **Monitoring & metering** — net meter, SCADA dashboard, CT/PT unit
8. **Civil & installation** — foundation/fixing, cable trays, labour
9. **Approvals, testing & commissioning** — structural certificate, DISCOM liaison, insulation/earth/PR tests

**Typical cost split:** Modules ~55-60% | Inverters ~10-12% | BOS/structure ~15-18% | Cabling/civil/testing ~remainder

---

## 7. Physics Reference (for explaining *why*, not just *what*)

- **P-n junction / depletion region** — diffusion of carriers across doped silicon leaves fixed ionized atoms behind, creating a permanent built-in electric field that separates photon-generated electron-hole pairs before they recombine
- **Bandgap (silicon ~1.1 eV)** — minimum photon energy needed to free an electron; below-bandgap photons pass through unabsorbed (why tandem cells stack a second material)
- **Contact recombination** — the main loss PERC never solved; TOPCon fixes it with an ultra-thin tunnel oxide (quantum tunneling lets carriers through) + a doped polysilicon selective contact layer
- **Temperature coefficient** — physical basis for why HJT/hot-climate matching matters
- **PID mechanism** — stray leakage voltage across the module frame/encapsulation gradually disturbs the same junction field, causing slow output decline — this is why MQT21 exists

---

## 8. Terminology Index (quick lookup)

CUF, PR, PSH, kWp, BOS, MPPT, DC:AC ratio, EPC, RESCO, PPA, LCOE, IRR, NPV, DISCOM, SERC, MNRE, ALMM, BIS, PID, LID, LeTID, UVID, MQT, PVEL/PQP, RETC, EL testing, TOPCon, HJT, IBC/BC, PERC, Mono/Poly/Thin-film, bifacial, half-cut, glass-glass vs glass-backsheet, ACDB, MCCB, CT/PT, IS 875, IS 3043, NOC, empanelment, cross-subsidy surcharge, wheeling charges, virtual net metering, group captive (26% rule), banking, curtailment.

*(Full plain-English definitions for each of these were built out earlier in this knowledge thread — this index is for quick tool-reference lookup once definitions are loaded elsewhere in the system.)*
