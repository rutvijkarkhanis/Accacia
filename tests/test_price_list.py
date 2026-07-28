from datetime import date

import pytest

from accacia.price_list import (
    DEFAULT_STALE_DAYS,
    SEED_DATE,
    PriceEntry,
    default_price_list,
    find_entry,
    stale_entries,
)
from accacia.vendors import VENDORS


def test_default_list_mirrors_vendor_roster():
    pl = default_price_list()
    assert [e.brand for e in pl] == [v.name for v in VENDORS]
    assert all(e.indicative for e in pl)
    assert all(e.last_updated == SEED_DATE for e in pl)
    # notable models flow through where the roster has them
    adani = find_entry(pl, "Adani Solar")
    assert adani.model == "ASB-M10-144-AAA"


def test_days_since_and_staleness():
    e = PriceEntry("X", "m", 580, 22.0, date(2026, 1, 1), indicative=False)
    assert e.days_since_update(today=date(2026, 1, 31)) == 30
    assert not e.is_stale(today=date(2026, 1, 31))          # 30 < 90 days
    assert e.is_stale(today=date(2026, 6, 1))               # > 90 days


def test_indicative_is_always_stale():
    e = PriceEntry("X", "m", 580, 23.0, date.today(), indicative=True)
    # even freshly dated, an indicative (unconfirmed) price counts as stale
    assert e.is_stale()


def test_find_entry_by_brand_and_model():
    pl = default_price_list()
    assert find_entry(pl, "waaree") is not None            # case-insensitive
    assert find_entry(pl, "Adani Solar", "ASB-M10-144-AAA") is not None
    assert find_entry(pl, "Adani Solar", "wrong-model") is None
    assert find_entry(pl, "Nonexistent") is None


def test_stale_entries_flags_old_and_indicative():
    pl = default_price_list()
    # all seeded entries are indicative -> all stale
    assert len(stale_entries(pl)) == len(pl)
    # a freshly confirmed price is not stale
    pl[0] = PriceEntry(pl[0].brand, pl[0].model, 580, 22.0, date.today(),
                       indicative=False)
    assert pl[0] not in stale_entries(pl)
