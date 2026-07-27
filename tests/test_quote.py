import pytest

from accacia.quote import Enquiry, build_quote
from accacia.specs import SiteConditions


def test_end_to_end_quote():
    enquiry = Enquiry(
        site_area_sqft=20000,
        location="Ahmedabad",
        sanctioned_load_kva=250,
        conditions=SiteConditions(climate="hot", payback_focused=True),
    )
    quote = build_quote(enquiry)

    assert quote.site.feasible_capacity_kwp > 0
    # hot climate is higher priority than payback → HJT recommendation
    assert quote.spec.rule == "hot-climate"
    assert quote.finance.capex > 0
    # BOQ is generated and its line costs reconcile to the CAPEX
    assert len(quote.boq.lines) == 9
    assert sum(ln.cost for ln in quote.boq.lines) == pytest.approx(quote.finance.capex)
    # the §2 recommendation flows into the module line spec
    assert "HJT" in next(
        ln for ln in quote.boq.lines if ln.item == "Modules"
    ).spec
    summ = quote.summary()
    assert "SITE" in summ and "BOQ" in summ


def test_quote_to_dict_serialisable():
    import json

    quote = build_quote(Enquiry(site_area_sqft=15000, psh=5.5))
    d = quote.to_dict()
    # round-trips through JSON without error
    json.loads(json.dumps(d, default=str))
    assert "rows" in d["finance"]
    assert len(d["finance"]["rows"]) == quote.finance.tenure_years
    assert len(d["boq"]["lines"]) == 9


def test_finance_overrides_flow_through():
    quote = build_quote(
        Enquiry(site_area_sqft=15000, psh=5.5,
                finance_overrides={"cost_per_watt": 35, "tenure_years": 10})
    )
    assert quote.finance.tenure_years == 10
    assert quote.finance.capex == quote.site.feasible_capacity_kwp * 1000 * 35
