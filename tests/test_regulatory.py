import pytest

from accacia.regulatory import (
    compliance_checklist,
    recommend_commercial_model,
    recommend_grid_connection,
)


def test_standard_rooftop_net_metering():
    rec = recommend_grid_connection(200)
    assert rec.rule == "net-metering"


def test_over_cap_goes_open_access():
    rec = recommend_grid_connection(1500, state_net_metering_cap_kwp=1000)
    assert rec.choice == "Open access"
    assert rec.rule == "over-cap"


def test_insufficient_roof_open_access():
    rec = recommend_grid_connection(200, roof_sufficient=False)
    assert rec.rule == "open-access"


def test_group_captive_beats_cap_check():
    # joint ownership is decided before the capacity/cap check
    rec = recommend_grid_connection(200, multiple_consumers=True)
    assert rec.choice == "Group captive"
    assert "26%" in rec.reason


def test_sell_all_gross_metering():
    rec = recommend_grid_connection(200, sell_all_generation=True)
    assert rec.choice == "Gross metering"


def test_capex_when_capital_and_risk_and_upfront_ok():
    rec = recommend_commercial_model(
        has_capital=True, tax_appetite=True,
        wants_zero_upfront=False, can_absorb_performance_risk=True,
    )
    assert rec.rule == "capex"
    assert "accelerated depreciation" in rec.reason


def test_capex_without_tax_appetite_flags_it():
    rec = recommend_commercial_model(
        has_capital=True, tax_appetite=False,
        wants_zero_upfront=False, can_absorb_performance_risk=True,
    )
    assert rec.rule == "capex"
    assert "no tax appetite" in rec.reason.lower()


def test_resco_when_zero_upfront_wanted():
    rec = recommend_commercial_model(
        has_capital=True, tax_appetite=True,
        wants_zero_upfront=True, can_absorb_performance_risk=True,
    )
    assert rec.rule == "resco"


def test_resco_when_no_capital():
    rec = recommend_commercial_model(
        has_capital=False, tax_appetite=False,
        wants_zero_upfront=False, can_absorb_performance_risk=False,
    )
    assert rec.rule == "resco"


def test_compliance_checklist_regions():
    assert any("BIS" in item for item in compliance_checklist("india"))
    assert any("DEWA" in item for item in compliance_checklist("gcc"))
    with pytest.raises(ValueError):
        compliance_checklist("europe")
