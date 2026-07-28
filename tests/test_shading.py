import math

import pytest

from accacia.shading import (
    inter_row_shading,
    winter_solstice_noon_altitude,
)


def test_winter_solstice_altitude():
    # latitude 28 (Delhi belt): 90 - 28 - 23.5 = 38.5 degrees
    assert winter_solstice_noon_altitude(28) == pytest.approx(38.5)


def test_flush_mount_needs_no_spacing():
    # a flat (zero-tilt) row casts no shadow: gap 0, GCR 1, no layout loss
    r = inter_row_shading(2.0, tilt_deg=0, latitude_deg=28)
    assert r.inter_row_gap_m == pytest.approx(0)
    assert r.ground_coverage_ratio == pytest.approx(1.0)
    assert r.layout_loss_fraction == pytest.approx(0)


def test_geometry_matches_hand_calc():
    # L=2 m, tilt 15, latitude 28 -> altitude 38.5
    r = inter_row_shading(2.0, tilt_deg=15, latitude_deg=28)
    assert r.row_height_m == pytest.approx(2 * math.sin(math.radians(15)), rel=1e-6)
    assert r.horizontal_base_m == pytest.approx(2 * math.cos(math.radians(15)), rel=1e-6)
    expected_gap = r.row_height_m / math.tan(math.radians(38.5))
    assert r.inter_row_gap_m == pytest.approx(expected_gap, rel=1e-6)
    assert r.row_pitch_m == pytest.approx(r.horizontal_base_m + r.inter_row_gap_m)
    assert r.ground_coverage_ratio == pytest.approx(2.0 / r.row_pitch_m)
    # layout loss equals the gap's share of the pitch
    assert r.layout_loss_fraction == pytest.approx(r.inter_row_gap_m / r.row_pitch_m)
    # a typical flat-roof design lands around GCR 0.4-0.8
    assert 0.4 < r.ground_coverage_ratio < 0.9


def test_higher_tilt_widens_spacing_and_lowers_gcr():
    low = inter_row_shading(2.0, tilt_deg=10, latitude_deg=28)
    high = inter_row_shading(2.0, tilt_deg=25, latitude_deg=28)
    assert high.inter_row_gap_m > low.inter_row_gap_m
    assert high.ground_coverage_ratio < low.ground_coverage_ratio


def test_lower_latitude_needs_less_spacing():
    # nearer the equator the winter sun is higher, so shadows are shorter
    north = inter_row_shading(2.0, tilt_deg=15, latitude_deg=30)
    south = inter_row_shading(2.0, tilt_deg=15, latitude_deg=13)
    assert south.inter_row_gap_m < north.inter_row_gap_m


def test_explicit_solar_altitude_overrides_latitude():
    r = inter_row_shading(2.0, tilt_deg=15, solar_altitude_deg=45)
    assert r.solar_altitude_deg == 45
    assert r.latitude_deg is None


def test_invalid_inputs():
    with pytest.raises(ValueError):
        inter_row_shading(-1, tilt_deg=15, latitude_deg=28)
    with pytest.raises(ValueError):
        inter_row_shading(2.0, tilt_deg=90, latitude_deg=28)
    with pytest.raises(ValueError):
        inter_row_shading(2.0, tilt_deg=15)  # neither latitude nor altitude
    with pytest.raises(ValueError):
        # extreme latitude -> winter-noon sun below horizon
        inter_row_shading(2.0, tilt_deg=15, latitude_deg=70)
