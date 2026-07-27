# Competitive Landscape — What Established Solar Software Does, and What Accacia Can Adopt

This note surveys what the widely used solar design and proposal platforms do
that a spreadsheet or a first-generation quoting engine does not, and then maps
each capability to whether Accacia can realistically adopt it, and at what cost.
Acronyms are spelled out on first use.

## The players and their signature strengths

- **PVsyst** — the bankability reference standard. A desktop tool that runs an
  hour-by-hour simulation over all 8,760 hours of a typical meteorological year,
  builds a three-dimensional near-shading model, and produces a full loss diagram
  (temperature, soiling, mismatch, wiring, inverter clipping, shading, and more).
  Lenders and Detailed Project Reports expect PVsyst output for large projects.
- **Aurora Solar** — remote design from aerial and Light Detection and Ranging
  (LiDAR) imagery. It reconstructs the roof in three dimensions, detects
  obstructions automatically, runs an automated shading analysis without a site
  visit, and generates a branded proposal. Strong sales-to-design workflow.
- **HelioScope** (now part of Aurora) — fast commercial and industrial array
  layout, automatic stringing, single-line electrical diagrams, and
  component-level energy simulation. Popular for the exact 100 kilowatt to 1
  megawatt segment Accacia targets.
- **PV*SOL** — three-dimensional shading simulation with strong visualisation of
  how shadows move across the array through the day and year.
- **OpenSolar** — free design plus proposal plus hardware-ordering platform with a
  built-in customer relationship management pipeline; strong for residential and
  small commercial.
- **SolarEdge Designer, Enphase Solargraf, and Pylon** — vendor and third-party
  proposal tools that produce quick layouts, proposals, financing options, and
  electronic signature flows.

## Capability-by-capability: what they do, and what Accacia can do

| Capability they have | What it means | Can Accacia do it? | Effort |
|---|---|---|---|
| Satellite and Light Detection and Ranging roof capture | Auto-measure roof area and detect obstructions remotely, no site visit | Partly — call the Google Solar Application Programming Interface or a map-polygon tool to estimate area and rough obstructions | Medium |
| Automated shading analysis | Compute shading loss from a three-dimensional model or a fisheye sky photograph | Partly — implement the inter-row-spacing and Ground Coverage Ratio calculator now (documented in Section 1); full three-dimensional shading later | Easy now / Hard later |
| Hour-by-hour (8,760-hour) simulation with a loss diagram | Replace a single Performance Ratio with an itemised set of losses | Yes — build a monthly or hourly model that breaks out temperature, soiling, shading, mismatch, wiring, and inverter-clipping losses | Medium |
| Site-specific weather data | Use a real typical-meteorological-year dataset for the exact coordinates rather than a regional average | Yes — integrate the free Photovoltaic Geographical Information System Application Programming Interface to replace the static Peak Sun Hours lookup table | Medium |
| Electricity-bill parsing and tariff modelling | Read consumption and tariff from uploaded bills; model Time-of-Use rates and a target offset percentage | Yes — add a consumption-and-tariff module; bill parsing can be manual entry first, automated later | Medium |
| Automatic layout and stringing | Place panels and wire strings to inverter Maximum Power Point Tracker channels automatically | Not yet — needs geometry and a component database; low priority for a quoting tool | Hard |
| Real component database | Choose from actual module and inverter models with datasheets and Approved List of Models and Manufacturers status | Yes — add a curated data file of real modules and inverters and drive the Bill of Quantities from it | Medium |
| Branded proposal generation | Produce a polished, client-ready Portable Document Format proposal | Yes — Accacia already produces a structured quote; render it to a branded document | Easy–Medium |
| Financing, loan, and electronic-signature flows | Model loans and collect signatures inside the tool | Partly — Accacia already computes payback, Internal Rate of Return, and Net Present Value; add loan and monthly-instalment modelling; signatures are out of scope | Medium |

## Recommended order of adoption for Accacia

The highest value for the least effort, in order:

1. **Inter-row shading and Ground Coverage Ratio calculator.** The method is
   already documented in Section 1; turning it into a function is small and
   directly improves the area and layout estimate. *(Easy.)*
2. **Site-specific weather data via the Photovoltaic Geographical Information
   System.** Replace the regional Peak Sun Hours midpoints with a real dataset for
   the coordinates. This is the single biggest accuracy upgrade. *(Medium.)*
3. **A proper loss breakdown** in place of the single Performance Ratio —
   temperature, soiling, shading, mismatch, wiring, and inverter clipping — so the
   generation estimate is defensible and transparent. *(Medium.)*
4. **Consumption-and-tariff modelling** from twelve months of bills, including a
   target offset percentage and Time-of-Use rates. *(Medium.)*
5. **A branded proposal document** rendered from the existing quote. *(Easy–Medium.)*
6. **A real module and inverter database** driving the Bill of Quantities.
   *(Medium.)*

## Deliberately out of scope for now

- Full three-dimensional roof reconstruction from Light Detection and Ranging, and
  automatic panel layout and stringing. These need heavy geometry, computer vision,
  and large datasets, and add little to a *quoting* tool whose job ends at a firm
  number and a Bill of Quantities.
- Electronic-signature and payment collection — a customer-relationship-management
  concern, not an engineering one.
