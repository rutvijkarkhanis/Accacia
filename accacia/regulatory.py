"""Section 4 Regulatory & Commercial Structuring — selectors and checklists.

Encodes the grid-connection mechanism table, the CAPEX-vs-RESCO commercial
model selector, and the India/GCC compliance checklists from
``sections/04-regulatory-commercial.md``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Region = Literal["india", "gcc"]

# Default state net-metering cap (kWp). The KB notes this varies by state,
# often 500 kW–1 MW; 1 MW is used as a permissive default — override per state.
DEFAULT_STATE_NET_METERING_CAP_KWP = 1000.0


@dataclass
class Recommendation:
    choice: str
    reason: str
    rule: str


def recommend_grid_connection(
    capacity_kwp: float,
    *,
    state_net_metering_cap_kwp: float = DEFAULT_STATE_NET_METERING_CAP_KWP,
    roof_sufficient: bool = True,
    multiple_consumers: bool = False,
    sell_all_generation: bool = False,
) -> Recommendation:
    """Pick a grid-connection mechanism (Section 4 table).

    Priority: a structural fact (selling all generation, joint ownership,
    insufficient roof) outranks the default net-metering path, which itself
    depends on staying under the state cap.
    """
    if sell_all_generation:
        return Recommendation(
            "Gross metering",
            "All generation is sold separately from consumption billing "
            "(rare now, but this is the case it fits).",
            "sell-all",
        )
    if multiple_consumers:
        return Recommendation(
            "Group captive",
            "Multiple consumers jointly own ≥26% of the plant, seeking "
            "open-access tariff benefits (26% rule).",
            "group-captive",
        )
    if not roof_sufficient:
        return Recommendation(
            "Open access",
            "Roof space is insufficient — source from an off-site plant as a "
            "large consumer via open access.",
            "open-access",
        )
    if capacity_kwp > state_net_metering_cap_kwp:
        return Recommendation(
            "Open access",
            f"Capacity {capacity_kwp:,.0f} kWp exceeds the state net-metering "
            f"cap ({state_net_metering_cap_kwp:,.0f} kWp) — net metering unavailable.",
            "over-cap",
        )
    return Recommendation(
        "Net metering",
        "Standard C&I rooftop under the state capacity cap.",
        "net-metering",
    )


def recommend_commercial_model(
    *,
    has_capital: bool,
    tax_appetite: bool,
    wants_zero_upfront: bool,
    can_absorb_performance_risk: bool,
) -> Recommendation:
    """Pick CAPEX/EPC vs RESCO/PPA (Section 4 commercial model selector).

    ``tax_appetite`` = the client has enough taxable profit to absorb
    accelerated depreciation — a qualifying question before pitching CAPEX.
    """
    capex_fit = has_capital and can_absorb_performance_risk and not wants_zero_upfront
    if capex_fit:
        reason = (
            "Client has capital and can absorb performance risk, wants 100% of "
            "savings after payback"
        )
        reason += (
            " and has the tax appetite to use accelerated depreciation."
            if tax_appetite
            else " (no tax appetite — accelerated depreciation won't apply, "
            "check the payback still stands)."
        )
        return Recommendation("CAPEX / EPC", reason, "capex")

    return Recommendation(
        "RESCO / PPA",
        "Client wants zero upfront cost and to de-risk completely, accepting a "
        "capped long-term savings ceiling; developer carries the balance sheet.",
        "resco",
    )


# Section 4 compliance checklists — the legal gatekeepers and credibility filters.
INDIA_COMPLIANCE: list[str] = [
    "BIS certification — IS 14286 (modules) / IS 16221 & IS 16169 (inverters), mandatory",
    "ALMM listing — exact model number, required for subsidy/govt-linked projects; "
    "verify at point of procurement",
    "MNRE empanelment — per DISCOM/state, doesn't auto-extend across regions",
    "Structural safety certificate — licensed engineer sign-off before mounting",
    "GST/EPFO/MCA21 clean record — informal but real credibility filter in tenders",
]

GCC_COMPLIANCE: list[str] = [
    "DEWA-certified contractor (Category A/B/C by system size)",
    "DEWA-approved equipment list",
    "Shams Dubai net metering pathway via Hab Reeh platform",
    "Note: each UAE emirate runs its own utility program (DEWA ≠ ADDC ≠ EtihadWE) "
    "under a shared federal framework — no single GCC-wide rule",
]

# Key PPA clauses to always check for (Section 4).
PPA_CLAUSES: list[str] = [
    "Tariff structure (fixed vs escalating)",
    "Minimum guaranteed generation / PR floor with compensation clause",
    "Contract tenure (15–25 yrs)",
    "Termination/buyout clause and lock-in period",
    "Curtailment risk allocation (DISCOM export caps / banking rule changes)",
    "O&M SLA (uptime %, response time, penalties)",
]


def compliance_checklist(region: Region = "india") -> list[str]:
    """Return the compliance checklist for a region (``india`` or ``gcc``)."""
    if region == "india":
        return list(INDIA_COMPLIANCE)
    if region == "gcc":
        return list(GCC_COMPLIANCE)
    raise ValueError(f"unknown region {region!r}; use 'india' or 'gcc'")
