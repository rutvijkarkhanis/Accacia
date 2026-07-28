import math

import pytest

from accacia.boq import COST_SPLIT, build_boq


def test_cost_split_sums_to_one():
    assert abs(sum(COST_SPLIT.values()) - 1.0) < 1e-9


def test_line_costs_sum_to_capex():
    boq = build_boq(200, capex=8_000_000)
    total = sum(ln.cost for ln in boq.lines)
    assert total == pytest.approx(8_000_000)
    assert len(boq.lines) == 9


def test_module_count_covers_capacity():
    boq = build_boq(200, capex=8_000_000, module_wp=580)
    # 200 kWp / 580 Wp = 344.8 → rounds up to fully cover capacity
    assert boq.module_count == math.ceil(200 * 1000 / 580)
    assert boq.module_count * 580 >= 200 * 1000


def test_inverter_count_from_dc_ac_ratio():
    boq = build_boq(200, capex=8_000_000, inverter_kw=100, dc_ac_ratio=1.2)
    # AC capacity = 200 / 1.2 = 166.7 kW → 2 × 100 kW inverters
    assert boq.ac_capacity_kwp == pytest.approx(200 / 1.2)
    assert boq.inverter_count == math.ceil((200 / 1.2) / 100)


def test_modules_are_largest_line():
    boq = build_boq(200, capex=8_000_000)
    module_line = next(ln for ln in boq.lines if ln.item == "Modules")
    assert module_line.pct_of_capex == pytest.approx(0.575)
    assert module_line.cost == max(ln.cost for ln in boq.lines)


def test_cell_tech_appears_in_module_spec():
    boq = build_boq(200, capex=8_000_000, cell_tech="HJT", bom=None)
    module_line = next(ln for ln in boq.lines if ln.item == "Modules")
    assert "HJT" in module_line.spec


def test_bom_overrides_cell_tech_in_spec():
    boq = build_boq(200, capex=8_000_000, cell_tech="HJT", bom="Custom bifacial BOM")
    module_line = next(ln for ln in boq.lines if ln.item == "Modules")
    assert "Custom bifacial BOM" in module_line.spec


def test_unit_cost_only_for_countable_lines():
    boq = build_boq(200, capex=8_000_000)
    module_line = next(ln for ln in boq.lines if ln.item == "Modules")
    bos_line = next(ln for ln in boq.lines if ln.item.startswith("Mounting"))
    assert module_line.unit_cost() is not None
    assert bos_line.unit_cost() is None


def test_invalid_inputs():
    with pytest.raises(ValueError):
        build_boq(-1, capex=1000)
    with pytest.raises(ValueError):
        build_boq(200, capex=-1)
    with pytest.raises(ValueError):
        build_boq(200, capex=1000, dc_ac_ratio=0)


def test_module_rate_prices_module_line_directly():
    # capex = 200 kWp * 1000 * (23 + 17) = 8,000,000
    boq = build_boq(200, capex=8_000_000, module_rate_per_watt=23.0, module_wp=580)
    module = next(ln for ln in boq.lines if ln.item == "Modules")
    expected = boq.module_count * 580 * 23.0
    assert module.cost == pytest.approx(expected)
    # lines still reconcile to the total capex
    assert sum(ln.cost for ln in boq.lines) == pytest.approx(8_000_000)


def test_brand_appears_in_module_spec_and_header():
    boq = build_boq(200, capex=8_000_000, brand="Adani Solar",
                    brand_tier="7/8 PVEL designations", module_rate_per_watt=23.0)
    module = next(ln for ln in boq.lines if ln.item == "Modules")
    assert "Adani Solar" in module.spec
    assert boq.brand == "Adani Solar"
    assert "Adani Solar" in boq.summary()


def test_module_rate_zero_falls_back_to_split():
    # a zero module rate can't exceed capex; module line becomes 0 and the rest
    # absorb the total via the standard split without error
    boq = build_boq(200, capex=8_000_000, module_rate_per_watt=0.0)
    assert sum(ln.cost for ln in boq.lines) == pytest.approx(8_000_000)


def test_zero_capex_ok():
    # a spec-only sizing with no price still produces a valid 9-line BOQ
    boq = build_boq(200, capex=0)
    assert all(ln.cost == 0 for ln in boq.lines)
    assert boq.module_count > 0
