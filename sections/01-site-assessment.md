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
- Performance Ratio benchmark: 75 percent (below-average installation) / 80 percent (standard good Engineering, Procurement and Construction contractor) / 85 percent or higher (premium, well-monitored)
- Degradation: 2 to 2.5 percent first-year dip, then 0.4 to 0.5 percent per year for silicon; Heterojunction Technology trends toward the lower end (about 0.3 to 0.4 percent per year)

---

## How to Obtain Each Input — A Guide for the Client

Every number in a quote is only as good as the input behind it. Several of the
required inputs are not things you can guess from a desk — they must either be
measured on site, read off a document the site owner already holds, or requested
formally from the electricity distribution company. Below is exactly where each
one comes from, so the salesperson can guide the site owner through gathering it
before a quote is treated as firm.

**1. Available roof or land area (in square feet)**
- Where it comes from: an actual measurement, not an estimate. Three acceptable
  sources, in decreasing order of reliability — (a) the architectural roof plan
  or building drawings held by the owner; (b) a physical measurement taken during
  the site survey with a measuring tape or laser distance meter; (c) a
  first-pass satellite estimate by drawing a polygon over the roof in a mapping
  tool such as Google Earth.
- What to tell the owner: "Please share the building's roof plan or architectural
  drawings if you have them." If none exist, a site survey is required.
- What to deduct before using the number: walkways and maintenance access paths,
  edge setbacks required by fire and safety norms, areas already occupied by
  water tanks, air-conditioning units, skylights, and any zone that falls under a
  shadow (see the shading section below). The number that enters the calculation
  is the *clear, usable* area, not the gross roof area.

**2. Roof type (Reinforced Cement Concrete flat roof, metal sheet roof, or ground)**
- Where it comes from: the site survey, or simply asking the owner.
- Why it is requested: it decides the mounting structure (a ballasted or
  penetrating structure on a Reinforced Cement Concrete roof, versus clamps on a
  metal sheet roof), which in turn affects the Balance of System cost and the
  structural safety certificate. A metal sheet roof also needs its sheet
  thickness and the condition and age of the roof confirmed, because the panels
  will outlive a thin or corroded sheet.

**3. Sanctioned load or contract demand (in kilovolt-amperes)**
- Where it comes from: it is printed on the monthly electricity bill, usually
  labelled "Sanctioned Load", "Contract Demand", or "Connected Load". It also
  appears on the original sanction letter or connection agreement issued by the
  electricity distribution company.
- What to request from the owner: "Please share a recent electricity bill, or the
  connection sanction letter." A single recent bill is enough for this figure.
- Why it matters so much: the rooftop system capacity that the distribution
  company will allow you to connect and export is frequently capped at a
  percentage of the sanctioned load (commonly in the range of 100 to 200 percent,
  and set by each state's regulation), not by the roof area. This is why the
  capacity calculation takes the *smaller* of the roof-area limit and the
  sanctioned-load limit. If the sanctioned load is too small, the owner can apply
  to the distribution company for a load enhancement before the project proceeds.

**4. Average monthly consumption (in units, that is, kilowatt-hours) and the current tariff category**
- Where it comes from: twelve consecutive monthly electricity bills. Twelve months
  are needed rather than one so that seasonal swings (summer air-conditioning
  load, monsoon dips, holiday shutdowns) average out. Each bill states the units
  consumed and the tariff category (for example Low Tension or High Tension,
  commercial or industrial).
- What to request from the owner: "Please share the last twelve months of
  electricity bills." If only a few are available, flag the estimate as
  provisional.
- What to also note from the bill: whether a Time-of-Use or Time-of-Day tariff
  applies (different rates by hour), and the demand charges, because solar offsets
  energy charges but not always demand charges.

**5. Shading obstructions**
- Where it comes from: the site survey. Walk the roof and record every object that
  can cast a shadow — parapet walls, overhead water tanks, staircase and lift
  rooms, chimneys, cooling towers, adjacent taller buildings, trees, and telecom
  or transmission towers.
- What to record for each obstruction: its height above the roof surface, its
  horizontal distance from the proposed panel area, and its compass direction.
  Direction matters — in the northern hemisphere, obstructions on the southern
  side cast the longest shadows across the day and cost the most energy.
- See the detailed method for turning these observations into a loss percentage
  in the next section.

**6. Location (city, state, and ideally exact coordinates)**
- Where it comes from: the site address, or a dropped pin giving latitude and
  longitude.
- Why it is requested: the location fixes two independent things — the Peak Sun
  Hours (how much solar energy the site receives, from the table above or, better,
  from a site-specific resource dataset), and the regulatory regime (which
  electricity distribution company and which state rules apply, covered in
  Section 4).

---

## Calculating Shading and Layout Loss — Long Form

The single input labelled "shading loss" is doing two conceptually different jobs,
and it helps to separate them:

- **Layout loss** is the fraction of the roof or land area that cannot carry
  panels at all — access walkways, safety setbacks, the footprints of existing
  equipment, and the spacing left between tilted panel rows. It is an *area* loss.
- **Shading loss** in the strict sense is the fraction of *energy* lost because a
  shadow falls across panels that are installed. It is a *performance* loss.

In this tool the "shading loss" parameter is applied as an area derate (it shrinks
the usable area, and therefore the installable capacity), so it is best read as a
combined "layout and obstruction area derate". The purely energy-side shading that
remains after a sensible layout is folded into the Performance Ratio. When you have
a rigorous shading study, prefer to keep the two separate: use the area derate for
what you physically cannot cover, and lower the Performance Ratio for the energy the
surviving panels lose to intermittent shadow.

There are five methods for arriving at a defensible number, from quickest to most
rigorous. Use the lightest method that the deal size and the site clutter justify.

**Method 1 — Rule-of-thumb lookup (quick screening)**
- A clean, open roof with few obstructions loses roughly 5 to 8 percent to layout
  and shading combined. A cluttered roof — many water tanks, staircase rooms,
  neighbouring towers — loses 10 to 12 percent or more.
- Use this only for a first, non-binding screening quote, and say so.

**Method 2 — Solar-access measurement (site instrument)**
- On site, an instrument photographs the whole sky dome from the proposed panel
  location and overlays the sun's path across the year onto that photograph.
  Common instruments are the Solar Pathfinder and the Solmetric SunEye; several
  smartphone applications do the same with the phone's camera and tilt sensors.
- The instrument reports a "solar access" percentage for each month — the share of
  available sunlight that actually reaches that spot after obstructions.
- The shading loss is then simply: shading loss (percent) = 100 percent − solar
  access (percent). Take the annual-average solar access, weighted toward the
  months and hours that generate the most energy.

**Method 3 — Inter-row shading and Ground Coverage Ratio (for tilted rows on flat roofs and ground mounts)**
- When panels are tilted up in rows, each row casts a shadow northward onto the
  row behind it in the early morning and late afternoon. The design job is to
  space the rows far enough apart to avoid this shadow during the productive
  hours, without wasting so much roof that capacity collapses.
- Step 1 — height gained by the tilted row:
  ```
  Vertical height of the row, H = Panel length along the slope × sine(tilt angle)
  ```
- Step 2 — the sun's altitude angle at the design moment. The standard worst case
  is solar noon on the winter solstice (21 December), when the sun sits lowest:
  ```
  Solar altitude at winter-solstice noon, alpha = 90 degrees − site latitude − 23.5 degrees
  ```
  (The 23.5 degrees is the tilt of the Earth's axis. For a site at latitude 28
  degrees, alpha is about 38.5 degrees.)
- Step 3 — minimum shadow-free spacing between the base of one row and the base of
  the next:
  ```
  Minimum row spacing, D = H ÷ tangent(alpha)
  ```
- Step 4 — the Ground Coverage Ratio, which is the single number that captures the
  trade-off:
  ```
  Ground Coverage Ratio = Panel length along the slope ÷ Row pitch (D + panel base width)
  ```
  A high Ground Coverage Ratio packs more capacity onto the roof but increases
  inter-row shading loss; a low Ground Coverage Ratio wastes area but loses almost
  nothing to shading. Typical flat-roof designs settle around a Ground Coverage
  Ratio of 0.4 to 0.5. The area consumed by the spacing D is exactly the "layout
  loss" described above.

**Method 4 — Hour-by-hour three-dimensional simulation (bankable reports)**
- The rigorous method builds a three-dimensional model of the roof and every
  obstruction, then simulates the shadow across all 8,760 hours of the year and
  reports a near-shading loss factor. This is what professional simulation
  software (for example PVsyst, HelioScope, or Aurora) produces, and it is what a
  lender or a Detailed Project Report will expect for a large project.
- Adopt this method when the project value or the financing counterpart justifies
  the effort; its output is a defensible loss percentage plus a full loss diagram.

**Method 5 — Far-shading from the horizon profile (hilly or hemmed-in sites)**
- Distant obstructions — a ridline of hills, a wall of tall buildings — block the
  sun near sunrise and sunset for part of the year. This is captured as a horizon
  profile, either measured on site with a compass and an inclinometer, or
  downloaded for the coordinates from a public resource dataset such as the
  Photovoltaic Geographical Information System. It is added on top of the
  near-shading loss from Methods 2 to 4.

**Putting it together for the quote:**
- Combined derate to apply = layout loss (from Method 3 spacing and from
  unusable-area deductions) added to the near-shading and far-shading energy
  losses (from Methods 2, 4, and 5).
- For a screening quote, one combined figure of 5 to 12 percent from Method 1 is
  acceptable if labelled as provisional. For a firm quote on a meaningful project,
  measure the solar access (Method 2) or simulate it (Method 4), and keep the area
  loss and the energy loss separate as described.
