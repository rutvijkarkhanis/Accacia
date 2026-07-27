import math

import pytest

from accacia.site import (
    PSH_BY_REGION,
    annual_generation,
    assess_site,
    cuf_percent,
    feasible_capacity,
    lookup_psh,
)


def test_lookup_psh_exact_and_substring():
    assert lookup_psh("Ahmedabad") == PSH_BY_REGION["ahmedabad"]
    # substring match on a compound location string
    assert lookup_psh("Somewhere, Gujarat") == PSH_BY_REGION["gujarat"]


def test_lookup_psh_unknown_raises():
    with pytest.raises(KeyError):
        lookup_psh("Reykjavik")


def test_feasible_capacity_area_bound():
    usable, area_cap, load_cap, binding = feasible_capacity(
        20000, shading_loss=0.10, area_per_kwp=100
    )
    assert usable == pytest.approx(18000)
    assert area_cap == pytest.approx(180)
    assert load_cap is None
    assert binding == "roof area"


def test_feasible_capacity_load_bound():
    # roof allows 180 kWp, but sanctioned load caps at 120 kVA → load binds
    _, area_cap, load_cap, binding = feasible_capacity(
        20000, shading_loss=0.10, area_per_kwp=100, sanctioned_load_kva=120
    )
    assert area_cap == pytest.approx(180)
    assert load_cap == pytest.approx(120)
    assert binding == "sanctioned load"


def test_generation_and_cuf_consistent():
    gen = annual_generation(100, psh=5.5, pr=0.80)
    assert gen == pytest.approx(100 * 5.5 * 365 * 0.80)
    cuf = cuf_percent(100, gen)
    # CUF should equal PSH*PR*365/8760*100
    assert cuf == pytest.approx(5.5 * 0.80 * 365 / 8760 * 100)
    assert 15 < cuf < 22  # sane C&I range


def test_assess_site_picks_binding_constraint():
    site = assess_site(
        20000, location="Ahmedabad", pr=0.80, shading_loss=0.10,
        sanctioned_load_kva=120,
    )
    assert site.feasible_capacity_kwp == pytest.approx(120)
    assert site.binding_constraint == "sanctioned load"
    assert site.annual_generation_units > 0


def test_assess_site_requires_psh_or_location():
    with pytest.raises(ValueError):
        assess_site(20000)


def test_capacity_override():
    site = assess_site(20000, psh=5.5, capacity_override_kwp=150)
    assert site.feasible_capacity_kwp == 150
    assert site.binding_constraint == "manual override"


def test_invalid_inputs():
    with pytest.raises(ValueError):
        feasible_capacity(-1)
    with pytest.raises(ValueError):
        assess_site(20000, psh=5.5, pr=1.5)
