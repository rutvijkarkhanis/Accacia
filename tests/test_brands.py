import pytest

from accacia.brands import BRANDS, brand_names, get_brand
from accacia.vendors import VENDORS


def test_catalogue_mirrors_vendor_roster():
    assert brand_names() == [v.name for v in VENDORS]
    assert len(BRANDS) == len(VENDORS)


def test_get_brand_case_insensitive_and_tier():
    b = get_brand("adani solar")
    assert b.name == "Adani Solar"
    assert b.pvel_designations == 7
    assert "7/8" in b.tier()
    assert b.default_wp > 0
    assert b.indicative_rate_per_watt > 0


def test_roster_only_brand_tier_label():
    # a brand the KB doesn't quantify falls back to the roster label
    b = get_brand("Waaree")
    assert b.pvel_designations is None
    assert "roster" in b.tier().lower()


def test_unknown_brand_raises():
    with pytest.raises(KeyError):
        get_brand("Acme Panels")
