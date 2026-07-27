"""Enquiry → Quote orchestration.

Ties Section 1 site assessment, Section 2 spec selection, and Section 3 financials into one call,
turning the KB "required inputs from any enquiry" into a structured quote.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any

from .site import SiteAssessment, assess_site
from .specs import SiteConditions, SpecRecommendation, recommend_spec
from .finance import FinancialModel, run_financials
from .boq import BOQ, build_boq


@dataclass
class Enquiry:
    """The KB Section 1 required inputs, plus optional overrides for the models."""

    site_area_sqft: float
    location: str | None = None
    psh: float | None = None
    pr: float = 0.80
    sanctioned_load_kva: float | None = None
    shading_loss: float = 0.08
    area_per_kwp: float = 100.0
    capacity_override_kwp: float | None = None

    # Section 2 spec-driving conditions
    conditions: SiteConditions = field(default_factory=SiteConditions)

    # Section 3 financial overrides (defaults live in run_financials)
    finance_overrides: dict[str, Any] = field(default_factory=dict)

    # Section 6 BOQ overrides (module_wp, inverter_kw, dc_ac_ratio)
    boq_overrides: dict[str, Any] = field(default_factory=dict)


@dataclass
class Quote:
    enquiry: Enquiry
    site: SiteAssessment
    spec: SpecRecommendation
    finance: FinancialModel
    boq: BOQ

    def summary(self) -> str:
        return (
            "=== SITE ===\n" + self.site.summary()
            + "\n\n=== SPEC ===\n" + self.spec.summary()
            + "\n\n=== FINANCIALS ===\n" + self.finance.summary()
            + "\n\n=== BOQ ===\n" + self.boq.summary()
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "site": asdict(self.site),
            "spec": asdict(self.spec),
            "finance": {
                k: v for k, v in asdict(self.finance).items() if k != "rows"
            }
            | {"rows": [asdict(r) for r in self.finance.rows]},
            "boq": self.boq.to_dict(),
        }


def build_quote(enquiry: Enquiry) -> Quote:
    """Run the full enquiry-to-quote pipeline."""
    site = assess_site(
        enquiry.site_area_sqft,
        location=enquiry.location,
        psh=enquiry.psh,
        pr=enquiry.pr,
        shading_loss=enquiry.shading_loss,
        area_per_kwp=enquiry.area_per_kwp,
        sanctioned_load_kva=enquiry.sanctioned_load_kva,
        capacity_override_kwp=enquiry.capacity_override_kwp,
    )
    spec = recommend_spec(enquiry.conditions)
    finance = run_financials(
        site.feasible_capacity_kwp,
        site.annual_generation_units,
        **enquiry.finance_overrides,
    )
    boq = build_boq(
        site.feasible_capacity_kwp,
        finance.capex,
        cell_tech=spec.technology,
        bom=spec.bom,
        **enquiry.boq_overrides,
    )
    return Quote(enquiry=enquiry, site=site, spec=spec, finance=finance, boq=boq)
