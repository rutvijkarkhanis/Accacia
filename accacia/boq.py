"""§6 BOQ Structure — bill of quantities from a sized, priced plant.

Encodes the 9-line BOQ template and the typical cost split from
``sections/06-boq-template.md``. Given a capacity and total CAPEX, it allocates
cost across the line items, derives module and inverter counts, and stamps each
line with representative specs (referencing the standards the KB calls out).
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from math import ceil
from typing import Any

# Cost split (§6). Modules 55–60%, inverters 10–12%, BOS/structure 15–18%,
# cabling/civil/testing = remainder. Midpoints chosen; the six "remainder"
# lines sum to the leftover 15%. Percentages sum to 1.0 (asserted below).
COST_SPLIT: dict[str, float] = {
    "Modules": 0.575,
    "Inverters": 0.110,
    "Mounting structure (BOS)": 0.165,
    "DC cabling & protection": 0.035,
    "AC cabling & protection": 0.030,
    "Earthing & lightning protection": 0.015,
    "Monitoring & metering": 0.020,
    "Civil & installation": 0.030,
    "Approvals, testing & commissioning": 0.020,
}
assert abs(sum(COST_SPLIT.values()) - 1.0) < 1e-9, "COST_SPLIT must sum to 1.0"

DEFAULT_MODULE_WP = 580        # typical TOPCon module, 2026
DEFAULT_INVERTER_KW = 100      # representative C&I string inverter
DEFAULT_DC_AC_RATIO = 1.2      # KB range 1.1–1.3x


@dataclass
class BOQLine:
    item: str
    spec: str
    quantity: float | None      # None where a lump sum, not a countable qty
    unit: str | None
    cost: float
    pct_of_capex: float

    def unit_cost(self) -> float | None:
        if self.quantity and self.quantity > 0:
            return self.cost / self.quantity
        return None


@dataclass
class BOQ:
    capacity_kwp: float
    capex: float
    ac_capacity_kwp: float
    dc_ac_ratio: float
    module_wp: int
    module_count: int
    inverter_kw: float
    inverter_count: int
    lines: list[BOQLine] = field(default_factory=list)

    def summary(self) -> str:
        head = (
            f"BOQ — {self.capacity_kwp:,.1f} kWp DC / {self.ac_capacity_kwp:,.1f} kW AC "
            f"(DC:AC {self.dc_ac_ratio:g})\n"
            f"{self.module_count} × {self.module_wp} Wp modules  |  "
            f"{self.inverter_count} × {self.inverter_kw:g} kW inverters  |  "
            f"CAPEX ₹{self.capex:,.0f}"
        )
        rows = "\n".join(
            f"  {ln.item:<36} {('₹%0.0f' % ln.cost):>14}  {ln.pct_of_capex:>5.1%}"
            + (f"   ({ln.quantity:g} {ln.unit})" if ln.quantity and ln.unit else "")
            for ln in self.lines
        )
        return head + "\n" + rows

    def to_dict(self) -> dict[str, Any]:
        d = {k: v for k, v in asdict(self).items() if k != "lines"}
        d["lines"] = [asdict(ln) for ln in self.lines]
        return d


def build_boq(
    capacity_kwp: float,
    capex: float,
    *,
    cell_tech: str | None = None,
    bom: str | None = None,
    module_wp: int = DEFAULT_MODULE_WP,
    inverter_kw: float = DEFAULT_INVERTER_KW,
    dc_ac_ratio: float = DEFAULT_DC_AC_RATIO,
) -> BOQ:
    """Build a §6 bill of quantities for a sized, priced plant.

    ``cell_tech`` / ``bom`` come from the §2 spec recommendation and describe
    the module line; the rest of the plant is standard BOS. Costs are allocated
    from ``capex`` via ``COST_SPLIT``.
    """
    if capacity_kwp <= 0:
        raise ValueError("capacity_kwp must be positive")
    if capex < 0:
        raise ValueError("capex must be non-negative")
    if module_wp <= 0 or inverter_kw <= 0:
        raise ValueError("module_wp and inverter_kw must be positive")
    if dc_ac_ratio <= 0:
        raise ValueError("dc_ac_ratio must be positive")

    ac_capacity = capacity_kwp / dc_ac_ratio
    module_count = ceil(capacity_kwp * 1000 / module_wp)
    inverter_count = ceil(ac_capacity / inverter_kw)

    module_spec = bom or (
        f"{cell_tech or 'Mono TOPCon'}, half-cut; ALMM-listed model, product + "
        "performance warranty"
    )

    # Per-line spec text (§6 template) and countable quantities where meaningful.
    specs: dict[str, tuple[str, float | None, str | None]] = {
        "Modules": (f"{module_wp} Wp — {module_spec}", module_count, "nos"),
        "Inverters": (
            f"{inverter_kw:g} kW string inverter, MPPT channels, DC:AC "
            f"{dc_ac_ratio:g}, warranty",
            inverter_count,
            "nos",
        ),
        "Mounting structure (BOS)": (
            "Galvanised structure, tilt to latitude, wind load per IS 875",
            None,
            None,
        ),
        "DC cabling & protection": (
            "DC solar cable, combiner boxes, SPD, MC4 connectors",
            None,
            None,
        ),
        "AC cabling & protection": (
            "AC cable, ACDB, MCCB (step-up transformer if HT)",
            None,
            None,
        ),
        "Earthing & lightning protection": (
            "Earth pits per IS 3043, lightning arrestors",
            None,
            None,
        ),
        "Monitoring & metering": (
            "Net meter, SCADA dashboard, CT/PT unit",
            None,
            None,
        ),
        "Civil & installation": (
            "Foundation/fixing, cable trays, labour",
            None,
            None,
        ),
        "Approvals, testing & commissioning": (
            "Structural certificate, DISCOM liaison, insulation/earth/PR tests",
            None,
            None,
        ),
    }

    lines: list[BOQLine] = []
    for item, pct in COST_SPLIT.items():
        spec_text, qty, unit = specs[item]
        lines.append(
            BOQLine(
                item=item,
                spec=spec_text,
                quantity=qty,
                unit=unit,
                cost=capex * pct,
                pct_of_capex=pct,
            )
        )

    return BOQ(
        capacity_kwp=capacity_kwp,
        capex=capex,
        ac_capacity_kwp=ac_capacity,
        dc_ac_ratio=dc_ac_ratio,
        module_wp=module_wp,
        module_count=module_count,
        inverter_kw=inverter_kw,
        inverter_count=inverter_count,
        lines=lines,
    )
