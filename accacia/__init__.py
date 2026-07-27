"""Accacia — Solar EPC quoting engine.

Turns a C&I rooftop solar enquiry into a spec recommendation and a financial
model, encoding the logic from the Solar EPC Knowledge Bank (see ``sections/``):

- ``site``    — §1 capacity derivation and generation/CUF
- ``specs``   — §2 cell-technology decision matrix
- ``finance`` — §3 CAPEX / RESCO models, LCOE, IRR, NPV
- ``quote``   — orchestrates an enquiry into a full quote

All figures reflect India, 2026 defaults. Verify tariffs, ALMM/DISCOM rules,
and equipment listings at point of procurement.
"""

from .site import (
    PSH_BY_REGION,
    SiteAssessment,
    assess_site,
    lookup_psh,
)
from .specs import SpecRecommendation, recommend_spec
from .finance import (
    FinancialModel,
    YearRow,
    irr,
    lcoe,
    npv,
    run_financials,
)
from .boq import BOQ, BOQLine, COST_SPLIT, build_boq
from .regulatory import (
    Recommendation,
    compliance_checklist,
    recommend_commercial_model,
    recommend_grid_connection,
)
from .vendors import Vendor, recommend_vendors, shortlist_vendors
from .quote import Enquiry, Quote, build_quote

__version__ = "0.1.0"

__all__ = [
    "PSH_BY_REGION",
    "SiteAssessment",
    "assess_site",
    "lookup_psh",
    "SpecRecommendation",
    "recommend_spec",
    "FinancialModel",
    "YearRow",
    "irr",
    "lcoe",
    "npv",
    "run_financials",
    "BOQ",
    "BOQLine",
    "COST_SPLIT",
    "build_boq",
    "Recommendation",
    "compliance_checklist",
    "recommend_commercial_model",
    "recommend_grid_connection",
    "Vendor",
    "recommend_vendors",
    "shortlist_vendors",
    "Enquiry",
    "Quote",
    "build_quote",
    "__version__",
]
