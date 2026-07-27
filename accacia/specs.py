"""§2 Product/Spec Selection — cell-technology decision matrix.

Encodes the decision matrix and the cross-cutting default rule from
``sections/02-product-spec-selection.md`` as a small priority-ordered rule
engine. Each rule that fires contributes a recommendation and a reason; the
first-firing rule wins, and if none fire the KB default (Mono TOPCon base case)
is returned.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

Climate = Literal["hot", "moderate", "cool"]

# The KB base-case BOM — quoted when the buyer states no clear priority.
DEFAULT_BOM = "Mono TOPCon, half-cut, glass-backsheet, monofacial, PVEL Top Performer"


@dataclass
class SpecRecommendation:
    technology: str            # headline cell technology
    bom: str                   # suggested base BOM string
    reason: str                # why this rule fired
    upgrade_offer: str | None  # a clearly-priced upgrade tier to present
    rule: str                  # which matrix row / rule matched

    def summary(self) -> str:
        out = f"Recommended: {self.technology}\n  {self.reason}\n  BOM: {self.bom}"
        if self.upgrade_offer:
            out += f"\n  Upgrade tier: {self.upgrade_offer}"
        return out


@dataclass
class SiteConditions:
    """Buyer/site priorities that drive the matrix. Unset flags mean 'not a
    stated priority', which lets the KB default rule take over."""

    climate: Climate = "moderate"
    reflective_ground_mount: bool = False   # white gravel, light roofing, elevated
    space_constrained: bool = False          # small footprint, high load
    aesthetic_sensitive: bool = False        # visible facade, premium, BIPV
    long_hold: bool = False                  # keeps plant 20–25 yrs, lifetime yield
    payback_focused: bool = False            # 5–8 yr payback C&I buyer
    budget_sensitive: bool = False


def recommend_spec(cond: SiteConditions) -> SpecRecommendation:
    """Walk the §2 decision matrix in priority order and return the first match.

    Priority order reflects how binding each constraint is: a physical limit
    (space, reflective rear-gain, aesthetics) outranks a climate match, which
    outranks a pure cost/payback preference.
    """
    # 1. Roof space is the binding constraint → maximise watts/sqft.
    if cond.space_constrained:
        return SpecRecommendation(
            technology="HJT / IBC / BC-hybrid",
            bom="HJT or IBC, glass-glass, high-efficiency",
            reason="Roof space is the binding constraint — maximise watts/sqft "
            "when area, not budget, is the limiter.",
            upgrade_offer=None,
            rule="space-constrained",
        )

    # 2. Aesthetic-sensitive facade/BIPV → uniform black, no gridlines.
    if cond.aesthetic_sensitive:
        return SpecRecommendation(
            technology="IBC / Back Contact (BC)",
            bom="IBC/BC, glass-backsheet or glass-glass, all-black",
            reason="Aesthetic-sensitive mounting — no front gridlines, uniform "
            "black surface; bifaciality loss is irrelevant on flush/facade.",
            upgrade_offer=None,
            rule="aesthetic",
        )

    # 3. Reflective ground/elevated mount → capture rear-side light.
    if cond.reflective_ground_mount:
        return SpecRecommendation(
            technology="Bifacial TOPCon or HJT",
            bom="Bifacial TOPCon/HJT, glass-glass",
            reason="Elevated/ground mount over a reflective surface — captures "
            "rear-side reflected light a flush monofacial roof would waste.",
            upgrade_offer="HJT bifacial for lower degradation on a long hold",
            rule="reflective-mount",
        )

    # 4. Hot climate → protect generation against temperature loss.
    if cond.climate == "hot":
        return SpecRecommendation(
            technology="HJT (or TOPCon w/ strong temp coefficient)",
            bom="HJT, glass-glass, low temp-coefficient datasheet",
            reason="Hot climate / high roof temps — lower %/°C loss protects "
            "generation in high ambient heat.",
            upgrade_offer=None,
            rule="hot-climate",
        )

    # 5. Long-hold asset → degradation compounds; HJT pays off by yr 15–25.
    if cond.long_hold:
        return SpecRecommendation(
            technology="HJT",
            bom="HJT, glass-glass, low-degradation datasheet",
            reason="Long-hold asset — lower degradation compounds significantly "
            "by year 15–25, favouring lifetime yield over sticker price.",
            upgrade_offer=None,
            rule="long-hold",
        )

    # 6. Cool climate → HJT premium won't pay back; prefer TOPCon.
    if cond.climate == "cool":
        return SpecRecommendation(
            technology="TOPCon",
            bom=DEFAULT_BOM,
            reason="Cool/moderate climate, modest sun — HJT's heat advantage "
            "doesn't materialise; the premium doesn't pay back.",
            upgrade_offer=None,
            rule="cool-climate",
        )

    # 7. Payback-focused C&I buyer → TOPCon best balance.
    if cond.payback_focused:
        return SpecRecommendation(
            technology="TOPCon",
            bom=DEFAULT_BOM,
            reason="5–8 year payback focus — TOPCon is the best balance of cost, "
            "efficiency, bankability, and financing comfort in 2026.",
            upgrade_offer="HJT/bifacial as a clearly priced upgrade tier",
            rule="payback-focused",
        )

    # 8. Budget-sensitive standard rooftop → cheapest adequate ₹/W.
    if cond.budget_sensitive:
        return SpecRecommendation(
            technology="Mono PERC / TOPCon (monofacial)",
            bom="Mono PERC or TOPCon, half-cut, glass-backsheet, monofacial",
            reason="Standard flush rooftop, budget-sensitive — best ₹/W, mature "
            "supply chain, adequate for most C&I deals.",
            upgrade_offer="TOPCon PVEL Top Performer as a small step up",
            rule="budget-sensitive",
        )

    # Default rule — no clear priority stated → KB base case.
    return SpecRecommendation(
        technology="Mono TOPCon (base case)",
        bom=DEFAULT_BOM,
        reason="No single priority stated — quote the market-converged base "
        "case (TOPCon ~60–66% global share in 2026).",
        upgrade_offer="HJT/bifacial as a clearly priced upgrade tier",
        rule="default",
    )
