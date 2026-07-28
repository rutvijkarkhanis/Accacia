import pytest

from accacia.finance import irr, lcoe, npv, run_financials


def test_capex_and_payback_basic():
    fm = run_financials(
        100, annual_generation_units=160_600,  # ~100 kWp @ 5.5 PSH, 0.80 PR
        cost_per_watt=40, grid_tariff=8.5,
    )
    assert fm.capex == pytest.approx(100 * 1000 * 40)
    # a healthy C&I plant should pay back well within tenure
    assert fm.capex_payback_year is not None
    assert 3 <= fm.capex_payback_year <= 8


def test_first_year_no_degradation():
    fm = run_financials(100, 160_600, tenure_years=3)
    # year 1 generation equals the input (no degradation applied in year 1)
    assert fm.rows[0].generation_units == pytest.approx(160_600)
    # year 2 reflects the first-year dip
    assert fm.rows[1].generation_units < fm.rows[0].generation_units


def test_resco_savings_positive_and_below_capex():
    fm = run_financials(100, 160_600)
    # RESCO saves money every year (grid > resco rate) ...
    assert all(r.resco_savings > 0 for r in fm.rows)
    # ... but lifetime CAPEX savings exceed RESCO (KB: capped ceiling)
    assert fm.lifetime_capex_savings > fm.lifetime_resco_savings


def test_lcoe_reasonable_range():
    fm = run_financials(100, 160_600)
    # LCOE for C&I solar should land well under grid tariff
    assert 1.5 < fm.lcoe < 5.0


def test_irr_matches_npv_zero():
    fm = run_financials(100, 160_600)
    assert fm.irr is not None
    # NPV at the IRR should be ~0
    savings = [r.capex_savings for r in fm.rows]
    assert npv(fm.irr, fm.capex, savings) == pytest.approx(0, abs=1.0)


def test_irr_negative_when_savings_never_recover_capex():
    # tiny savings against a huge capex → a real but deeply negative IRR
    rate = irr(1_000_000, [1.0] * 25)
    assert rate is not None and rate < 0


def test_irr_none_when_all_cashflows_negative():
    # no positive cashflow anywhere → NPV never crosses zero → no IRR
    assert irr(1_000_000, [-100.0] * 25) is None


def test_npv_decreases_with_discount_rate():
    savings = [50_000] * 25
    assert npv(0.05, 1_000_000, savings) > npv(0.15, 1_000_000, savings)


def test_lcoe_zero_generation_raises():
    with pytest.raises(ValueError):
        lcoe(1000, [10], [0])
