"""Section 1 Site Assessment — capacity derivation and generation.

Encodes the capacity, generation, and CUF logic from
``sections/01-site-assessment.md``.
"""

from __future__ import annotations

from dataclasses import dataclass

# Peak Sun Hours (kWh/m²/day) by region — Section 1. Ranges in the KB are collapsed to
# a representative midpoint here; override with an explicit ``psh`` when known.
# Values are planning midpoints for annual daily PSH; site-specific resource
# assessment (satellite/ground data) should supersede them for a real quote.
PSH_BY_REGION: dict[str, float] = {
    # --- High resource (5.5–5.8): arid NW belt ---
    "rajasthan": 5.7,
    "jodhpur": 5.7,
    "jaisalmer": 5.75,
    "bikaner": 5.7,
    "jaipur": 5.6,
    "kutch": 5.7,
    "gujarat": 5.55,
    "ahmedabad": 5.55,
    "surat": 5.5,
    "vadodara": 5.5,
    "rajkot": 5.55,
    # --- Good resource (5.3–5.5): central & Deccan plateau ---
    "madhya pradesh": 5.45,
    "bhopal": 5.45,
    "indore": 5.45,
    "chhattisgarh": 5.4,
    "raipur": 5.4,
    "telangana": 5.4,
    "hyderabad": 5.4,
    "andhra pradesh": 5.4,
    "vijayawada": 5.4,
    "visakhapatnam": 5.35,
    "nagpur": 5.4,
    "aurangabad": 5.35,
    "chennai": 5.35,
    "tamil nadu": 5.35,
    "coimbatore": 5.4,
    "bengaluru": 5.25,
    "bangalore": 5.25,
    "karnataka": 5.25,
    # --- Moderate resource (5.0–5.2): Indo-Gangetic plains / NCR ---
    "delhi": 5.1,
    "delhi ncr": 5.1,
    "ncr": 5.1,
    "noida": 5.1,
    "gurgaon": 5.1,
    "gurugram": 5.1,
    "faridabad": 5.1,
    "haryana": 5.1,
    "uttar pradesh": 5.05,
    "lucknow": 5.05,
    "kanpur": 5.05,
    "punjab": 5.0,
    "ludhiana": 5.0,
    "amritsar": 5.0,
    "chandigarh": 5.05,
    "bihar": 5.0,
    "patna": 5.0,
    "odisha": 5.0,
    "bhubaneswar": 5.0,
    # --- Lower resource (4.8–5.0): humid coasts & monsoon belts ---
    "pune": 5.0,
    "mumbai": 4.9,
    "maharashtra": 4.95,
    "kerala": 4.95,
    "kochi": 4.95,
    "thiruvananthapuram": 4.95,
    "west bengal": 4.85,
    "kolkata": 4.85,
    "assam": 4.6,
    "guwahati": 4.6,
    # --- GCC ---
    "dubai": 5.7,
    "uae": 5.7,
    "abu dhabi": 5.75,
    "sharjah": 5.7,
}

DEFAULT_AREA_PER_KWP = 100.0  # sqft/kWp (KB range 90–110)
DEFAULT_SHADING_LOSS = 0.08   # 8% (KB range 5–12%)

# sqft consumed per kVA of sanctioned load, used only to convert a sanctioned
# load (kVA) into an equivalent kWp ceiling for the DISCOM cross-check.
# 1 kVA ≈ 1 kWp of interconnect headroom as a planning approximation.
KWP_PER_KVA = 1.0


def lookup_psh(location: str) -> float:
    """Return representative PSH for a location string, matching KB regions.

    Raises ``KeyError`` if the location isn't recognised — callers should pass
    an explicit PSH in that case.
    """
    key = location.strip().lower()
    if key in PSH_BY_REGION:
        return PSH_BY_REGION[key]
    # substring match so "Ahmedabad, Gujarat" still resolves
    for region, psh in PSH_BY_REGION.items():
        if region in key:
            return psh
    raise KeyError(
        f"No PSH mapping for {location!r}; pass an explicit psh value."
    )


@dataclass
class SiteAssessment:
    """Result of deriving feasible capacity and generation for a site."""

    usable_area_sqft: float
    area_capacity_kwp: float          # capacity the roof area allows
    load_cap_kwp: float | None        # DISCOM/sanctioned-load ceiling, if given
    feasible_capacity_kwp: float      # the binding minimum of the two
    binding_constraint: str           # "roof area" or "sanctioned load"
    annual_generation_units: float
    cuf_percent: float
    psh: float
    pr: float

    def summary(self) -> str:
        cap = f"{self.feasible_capacity_kwp:,.1f} kWp"
        return (
            f"Feasible capacity: {cap} (limited by {self.binding_constraint})\n"
            f"Year-1 generation: {self.annual_generation_units:,.0f} units  "
            f"| CUF {self.cuf_percent:.1f}%  | PSH {self.psh}  PR {self.pr:.0%}"
        )


def feasible_capacity(
    site_area_sqft: float,
    *,
    shading_loss: float = DEFAULT_SHADING_LOSS,
    area_per_kwp: float = DEFAULT_AREA_PER_KWP,
    sanctioned_load_kva: float | None = None,
) -> tuple[float, float, float | None, str]:
    """Return (usable_area, area_capacity, load_cap, binding_constraint).

    Capacity is the *minimum* of what the roof area allows and what the
    sanctioned load permits — the KB notes capacity is often capped by DISCOM
    connection limits, not just roof area.
    """
    if site_area_sqft <= 0:
        raise ValueError("site_area_sqft must be positive")
    if not 0 <= shading_loss < 1:
        raise ValueError("shading_loss must be in [0, 1)")
    if area_per_kwp <= 0:
        raise ValueError("area_per_kwp must be positive")

    usable_area = site_area_sqft * (1 - shading_loss)
    area_capacity = usable_area / area_per_kwp

    load_cap = None
    binding = "roof area"
    feasible = area_capacity
    if sanctioned_load_kva is not None:
        if sanctioned_load_kva <= 0:
            raise ValueError("sanctioned_load_kva must be positive")
        load_cap = sanctioned_load_kva * KWP_PER_KVA
        if load_cap < area_capacity:
            feasible = load_cap
            binding = "sanctioned load"

    return usable_area, area_capacity, load_cap, binding


def annual_generation(capacity_kwp: float, psh: float, pr: float) -> float:
    """Annual generation in units (kWh): Capacity × PSH × 365 × PR."""
    return capacity_kwp * psh * 365 * pr


def cuf_percent(capacity_kwp: float, annual_units: float) -> float:
    """Capacity Utilisation Factor: generation ÷ (capacity × 8760) × 100."""
    if capacity_kwp <= 0:
        raise ValueError("capacity_kwp must be positive")
    return annual_units / (capacity_kwp * 8760) * 100


def assess_site(
    site_area_sqft: float,
    *,
    location: str | None = None,
    psh: float | None = None,
    pr: float = 0.80,
    shading_loss: float = DEFAULT_SHADING_LOSS,
    area_per_kwp: float = DEFAULT_AREA_PER_KWP,
    sanctioned_load_kva: float | None = None,
    capacity_override_kwp: float | None = None,
) -> SiteAssessment:
    """Run the full Section 1 assessment for a site.

    Provide either ``location`` (looked up in ``PSH_BY_REGION``) or an explicit
    ``psh``. ``pr`` defaults to the KB "standard good EPC" benchmark of 80%.
    """
    if psh is None:
        if location is None:
            raise ValueError("provide either location or psh")
        psh = lookup_psh(location)
    if not 0 < pr <= 1:
        raise ValueError("pr must be in (0, 1]")

    usable, area_cap, load_cap, binding = feasible_capacity(
        site_area_sqft,
        shading_loss=shading_loss,
        area_per_kwp=area_per_kwp,
        sanctioned_load_kva=sanctioned_load_kva,
    )
    feasible = capacity_override_kwp if capacity_override_kwp else min(
        c for c in (area_cap, load_cap) if c is not None
    )
    if capacity_override_kwp:
        binding = "manual override"

    gen = annual_generation(feasible, psh, pr)
    return SiteAssessment(
        usable_area_sqft=usable,
        area_capacity_kwp=area_cap,
        load_cap_kwp=load_cap,
        feasible_capacity_kwp=feasible,
        binding_constraint=binding,
        annual_generation_units=gen,
        cuf_percent=cuf_percent(feasible, gen),
        psh=psh,
        pr=pr,
    )
