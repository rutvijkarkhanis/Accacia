"""§3 Financial Model — CAPEX / RESCO formula bank, LCOE, IRR, NPV.

Encodes the formulas from ``sections/03-financial-model.md``. Degradation is
modelled with a distinct first-year dip and a lower steady-state rate (KB: a
2–2.5% year-1 dip, then 0.4–0.5%/yr for silicon), rather than a single
compounding rate, so year-1 generation and payback are not overstated.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class YearRow:
    year: int
    generation_units: float
    grid_rate: float
    capex_om_cost: float
    capex_savings: float
    capex_cumulative: float
    resco_rate: float
    resco_savings: float
    resco_cumulative: float


@dataclass
class FinancialModel:
    capex: float
    tenure_years: int
    rows: list[YearRow] = field(default_factory=list)
    capex_payback_year: int | None = None       # None => no payback within tenure
    lifetime_generation_units: float = 0.0
    lifetime_capex_savings: float = 0.0
    lifetime_resco_savings: float = 0.0
    lcoe: float = 0.0
    irr: float | None = None                     # None => IRR undefined/not found
    npv: float = 0.0

    def summary(self) -> str:
        pay = (
            f"{self.capex_payback_year} yr"
            if self.capex_payback_year
            else f">{self.tenure_years} yr (none)"
        )
        irr_s = f"{self.irr:.1%}" if self.irr is not None else "n/a"
        return (
            f"CAPEX: ₹{self.capex:,.0f}  | Payback {pay}  | IRR {irr_s}\n"
            f"NPV ₹{self.npv:,.0f}  | LCOE ₹{self.lcoe:.2f}/unit\n"
            f"Lifetime CAPEX savings ₹{self.lifetime_capex_savings:,.0f}  "
            f"| Lifetime RESCO savings ₹{self.lifetime_resco_savings:,.0f}"
        )


def _degradation_factor(year: int, first_year_deg: float, annual_deg: float) -> float:
    """Fraction of nameplate PR retained in a given year (year 1 = 1.0)."""
    if year <= 1:
        return 1.0
    return (1 - first_year_deg) * (1 - annual_deg) ** (year - 2)


def lcoe(capex: float, om_costs: list[float], generation: list[float]) -> float:
    """LCOE (₹/unit) = total lifetime cost ÷ total lifetime generation.

    Simple (undiscounted) form per the KB definition. ``om_costs`` and
    ``generation`` are per-year lists over the tenure.
    """
    total_gen = sum(generation)
    if total_gen <= 0:
        raise ValueError("total generation must be positive")
    return (capex + sum(om_costs)) / total_gen


def npv(rate: float, capex: float, savings: list[float]) -> float:
    """NPV of the CAPEX case: -capex + Σ savings_y / (1+rate)^y."""
    value = -capex
    for y, s in enumerate(savings, start=1):
        value += s / (1 + rate) ** y
    return value


def irr(capex: float, savings: list[float]) -> float | None:
    """IRR of cashflows [-capex, savings_1, ...] via bisection.

    Returns the rate where NPV = 0, or ``None`` if no sign change exists in a
    plausible range (e.g. total savings never recover capex).
    """
    def f(rate: float) -> float:
        return npv(rate, capex, savings)

    lo, hi = -0.99, 10.0
    f_lo, f_hi = f(lo), f(hi)
    if f_lo == 0:
        return lo
    if f_hi == 0:
        return hi
    if f_lo * f_hi > 0:
        return None  # no sign change → no real IRR in range

    for _ in range(200):
        mid = (lo + hi) / 2
        f_mid = f(mid)
        if abs(f_mid) < 1e-6:
            return mid
        if f_lo * f_mid < 0:
            hi = mid
        else:
            lo, f_lo = mid, f_mid
    return (lo + hi) / 2


def run_financials(
    capacity_kwp: float,
    annual_generation_units: float,
    *,
    cost_per_watt: float = 40.0,
    grid_tariff: float = 8.5,
    tariff_escalation: float = 0.04,
    om_percent: float = 0.01,
    om_inflation: float = 0.05,
    resco_tariff_discount: float = 0.22,     # RESCO tariff = grid × (1 - discount)
    resco_escalation: float = 0.03,
    first_year_deg: float = 0.02,
    annual_deg: float = 0.005,
    tenure_years: int = 25,
    discount_rate: float = 0.10,
) -> FinancialModel:
    """Build the full year-by-year CAPEX and RESCO model.

    ``annual_generation_units`` is the year-1 (pre-degradation) figure from the
    site assessment; later years apply the degradation curve. Defaults sit
    inside the KB "India, 2026" assumption ranges.
    """
    if capacity_kwp <= 0:
        raise ValueError("capacity_kwp must be positive")
    if tenure_years < 1:
        raise ValueError("tenure_years must be >= 1")

    capex = capacity_kwp * 1000 * cost_per_watt
    resco_tariff0 = grid_tariff * (1 - resco_tariff_discount)

    rows: list[YearRow] = []
    capex_cum = -capex
    resco_cum = 0.0
    payback_year: int | None = None
    gen_list: list[float] = []
    om_list: list[float] = []
    capex_savings_list: list[float] = []

    for y in range(1, tenure_years + 1):
        gen = annual_generation_units * _degradation_factor(y, first_year_deg, annual_deg)
        grid_rate = grid_tariff * (1 + tariff_escalation) ** (y - 1)
        om_cost = capex * om_percent * (1 + om_inflation) ** (y - 1)
        capex_savings = gen * grid_rate - om_cost
        capex_cum += capex_savings

        resco_rate = resco_tariff0 * (1 + resco_escalation) ** (y - 1)
        resco_savings = gen * (grid_rate - resco_rate)
        resco_cum += resco_savings

        if payback_year is None and capex_cum >= 0:
            payback_year = y

        rows.append(
            YearRow(
                year=y,
                generation_units=gen,
                grid_rate=grid_rate,
                capex_om_cost=om_cost,
                capex_savings=capex_savings,
                capex_cumulative=capex_cum,
                resco_rate=resco_rate,
                resco_savings=resco_savings,
                resco_cumulative=resco_cum,
            )
        )
        gen_list.append(gen)
        om_list.append(om_cost)
        capex_savings_list.append(capex_savings)

    return FinancialModel(
        capex=capex,
        tenure_years=tenure_years,
        rows=rows,
        capex_payback_year=payback_year,
        lifetime_generation_units=sum(gen_list),
        lifetime_capex_savings=capex_cum + capex,   # Σ savings (add capex back out of cumulative)
        lifetime_resco_savings=resco_cum,
        lcoe=lcoe(capex, om_list, gen_list),
        irr=irr(capex, capex_savings_list),
        npv=npv(discount_rate, capex, capex_savings_list),
    )
