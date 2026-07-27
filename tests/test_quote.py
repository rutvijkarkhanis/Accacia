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
    # the Section 2 recommendation flows into the module line spec
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


def test_tilted_mount_derives_shading_from_layout_loss():
    flush = build_quote(Enquiry(site_area_sqft=20000, location="Ludhiana"))
    tilted = build_quote(Enquiry(
        site_area_sqft=20000, location="Ludhiana", mount_type="tilted",
    ))
    # a tilted mount needs inter-row spacing, so it fits less capacity than flush
    assert tilted.row_spacing is not None
    assert tilted.site.feasible_capacity_kwp < flush.site.feasible_capacity_kwp
    # the site's shading/area derate equals the computed inter-row layout loss
    used_derate = 1 - tilted.site.usable_area_sqft / 20000
    assert used_derate == pytest.approx(tilted.row_spacing.layout_loss_fraction)
    # mount block shows in the summary and serialises
    assert "MOUNT (tilted)" in tilted.summary()
    assert tilted.to_dict()["row_spacing"] is not None
    assert flush.to_dict()["row_spacing"] is None


def test_tilted_mount_uses_explicit_latitude_and_tilt():
    q = build_quote(Enquiry(
        site_area_sqft=20000, psh=5.0, mount_type="tilted",
        latitude_deg=28, tilt_deg=20,
    ))
    assert q.row_spacing.solar_altitude_deg == pytest.approx(90 - 28 - 23.5)
    assert q.row_spacing.tilt_deg == 20


def test_tilted_mount_without_latitude_or_location_errors():
    with pytest.raises(ValueError):
        build_quote(Enquiry(site_area_sqft=20000, psh=5.0, mount_type="tilted"))


def test_invalid_mount_type_errors():
    with pytest.raises(ValueError):
        build_quote(Enquiry(site_area_sqft=20000, psh=5.0, mount_type="floating"))


def test_brand_drives_cost_and_boq():
    q = build_quote(Enquiry(
        site_area_sqft=20000, psh=5.5, brand="Adani Solar",
        module_rate_per_watt=25, bos_rate_per_watt=18,
    ))
    # turnkey cost per watt = module_rate + bos_rate = 43
    assert q.finance.capex == pytest.approx(q.site.feasible_capacity_kwp * 1000 * 43)
    assert q.boq.brand == "Adani Solar"
    module = next(ln for ln in q.boq.lines if ln.item == "Modules")
    assert "Adani Solar" in module.spec
    # module line priced from the rate, and the BOQ still totals to capex
    assert module.cost == pytest.approx(q.boq.module_count * q.boq.module_wp * 25)
    assert sum(ln.cost for ln in q.boq.lines) == pytest.approx(q.finance.capex)


def test_brand_indicative_rate_used_when_no_explicit_rate():
    q = build_quote(Enquiry(site_area_sqft=20000, psh=5.5, brand="Waaree"))
    # indicative 23 + default bos 17 = 40 per watt
    assert q.finance.capex == pytest.approx(q.site.feasible_capacity_kwp * 1000 * 40)


def test_unknown_brand_errors():
    with pytest.raises(ValueError):
        build_quote(Enquiry(site_area_sqft=20000, psh=5.5, brand="Acme Panels"))


def test_finance_overrides_flow_through():
    quote = build_quote(
        Enquiry(site_area_sqft=15000, psh=5.5,
                finance_overrides={"cost_per_watt": 35, "tenure_years": 10})
    )
    assert quote.finance.tenure_years == 10
    assert quote.finance.capex == quote.site.feasible_capacity_kwp * 1000 * 35
