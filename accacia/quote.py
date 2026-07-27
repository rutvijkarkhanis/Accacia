"""Enquiry → Quote orchestration.

Ties Section 1 site assessment, Section 2 spec selection, and Section 3 financials into one call,
turning the KB "required inputs from any enquiry" into a structured quote.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any

from .site import SiteAssessment, assess_site, lookup_latitude
from .specs import SiteConditions, SpecRecommendation, recommend_spec
from .finance import FinancialModel, run_financials
from .boq import BOQ, build_boq
from .shading import RowSpacing, inter_row_shading

# Single module mounted in portrait, along-slope length in metres (typical
# 580 Wp module). Override per the actual table/row design.
DEFAULT_PANEL_SLANT_LENGTH_M = 2.3


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

    # Mounting: "flush" (panels parallel to the roof) or "tilted" (rows raised to
    # an angle, needing inter-row spacing). For a tilted mount the shading_loss
    # area derate is derived from the computed inter-row layout loss instead of
    # the manual default. tilt_deg defaults to the latitude; latitude_deg is
    # taken from the location when not given explicitly.
    mount_type: str = "flush"
    tilt_deg: float | None = None
    latitude_deg: float | None = None
    panel_slant_length_m: float = DEFAULT_PANEL_SLANT_LENGTH_M

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
    row_spacing: RowSpacing | None = None   # present only for tilted mounts

    def summary(self) -> str:
        out = (
            "=== SITE ===\n" + self.site.summary()
            + "\n\n=== SPEC ===\n" + self.spec.summary()
            + "\n\n=== FINANCIALS ===\n" + self.finance.summary()
            + "\n\n=== BOQ ===\n" + self.boq.summary()
        )
        if self.row_spacing is not None:
            out += "\n\n=== MOUNT (tilted) ===\n" + self.row_spacing.summary()
        return out

    def to_dict(self) -> dict[str, Any]:
        return {
            "site": asdict(self.site),
            "spec": asdict(self.spec),
            "finance": {
                k: v for k, v in asdict(self.finance).items() if k != "rows"
            }
            | {"rows": [asdict(r) for r in self.finance.rows]},
            "boq": self.boq.to_dict(),
            "row_spacing": asdict(self.row_spacing) if self.row_spacing else None,
        }


def _tilted_row_spacing(enquiry: Enquiry) -> RowSpacing:
    """Resolve latitude and tilt for a tilted mount and compute the row geometry."""
    latitude = enquiry.latitude_deg
    if latitude is None:
        if enquiry.location is None:
            raise ValueError(
                "a tilted mount needs a latitude — pass latitude_deg or a location"
            )
        try:
            latitude = lookup_latitude(enquiry.location)
        except KeyError as exc:
            raise ValueError(str(exc)) from exc
    # Rule of thumb: tilt roughly equals latitude when not stated.
    tilt = enquiry.tilt_deg if enquiry.tilt_deg is not None else latitude
    return inter_row_shading(
        enquiry.panel_slant_length_m, tilt_deg=tilt, latitude_deg=latitude
    )


def build_quote(enquiry: Enquiry) -> Quote:
    """Run the full enquiry-to-quote pipeline."""
    if enquiry.mount_type not in ("flush", "tilted"):
        raise ValueError("mount_type must be 'flush' or 'tilted'")

    # For a tilted mount, derive the area derate from the inter-row layout loss;
    # otherwise use the manual shading_loss. (Energy-side obstruction shading
    # remains folded into the performance ratio either way.)
    row_spacing: RowSpacing | None = None
    shading_loss = enquiry.shading_loss
    if enquiry.mount_type == "tilted":
        row_spacing = _tilted_row_spacing(enquiry)
        shading_loss = row_spacing.layout_loss_fraction

    site = assess_site(
        enquiry.site_area_sqft,
        location=enquiry.location,
        psh=enquiry.psh,
        pr=enquiry.pr,
        shading_loss=shading_loss,
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
    return Quote(
        enquiry=enquiry, site=site, spec=spec, finance=finance, boq=boq,
        row_spacing=row_spacing,
    )
