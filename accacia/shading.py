"""Inter-row shading and Ground Coverage Ratio geometry.

Encodes Method 3 from ``sections/01-site-assessment.md``: for tilted panel rows
on a flat roof or on the ground, work out the shadow-free spacing between rows,
the resulting Ground Coverage Ratio, and the area lost to that spacing (the
"layout loss" that feeds the capacity derate).

All lengths are in metres, all angles in degrees. The worst-case design moment
is solar noon on the winter solstice, when the sun sits lowest and shadows are
longest; pass an explicit ``solar_altitude_deg`` to design for a different time.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import cos, degrees, radians, sin, tan

# Tilt of the Earth's rotational axis, in degrees. It sets how much lower the
# sun sits at the winter solstice compared with the equinox.
EARTH_AXIAL_TILT_DEG = 23.5


@dataclass
class RowSpacing:
    """Geometry of a tilted row and the spacing it needs to avoid self-shading."""

    tilt_deg: float
    latitude_deg: float | None
    solar_altitude_deg: float
    panel_slant_length_m: float
    row_height_m: float            # vertical rise of the tilted row
    horizontal_base_m: float       # ground projection (footprint) of the row
    inter_row_gap_m: float         # clear shadow-free gap, back of one to front of next
    row_pitch_m: float             # base-to-base distance between successive rows
    ground_coverage_ratio: float   # slant length divided by pitch
    layout_loss_fraction: float    # share of ground area consumed by the spacing

    def summary(self) -> str:
        return (
            f"Tilt {self.tilt_deg:g} degrees at latitude "
            f"{self.latitude_deg if self.latitude_deg is not None else 'n/a'} "
            f"(sun altitude {self.solar_altitude_deg:.1f} degrees)\n"
            f"  Row rise {self.row_height_m:.2f} m, footprint "
            f"{self.horizontal_base_m:.2f} m\n"
            f"  Shadow-free gap {self.inter_row_gap_m:.2f} m, row pitch "
            f"{self.row_pitch_m:.2f} m\n"
            f"  Ground Coverage Ratio {self.ground_coverage_ratio:.2f}, "
            f"layout loss {self.layout_loss_fraction:.1%}"
        )


def winter_solstice_noon_altitude(latitude_deg: float) -> float:
    """Sun's altitude angle at solar noon on the winter solstice, in degrees.

    For the northern hemisphere this is ``90 - latitude - 23.5``. A negative or
    zero result would mean the sun never clears the horizon at noon, which the
    caller should treat as an invalid design latitude.
    """
    return 90.0 - latitude_deg - EARTH_AXIAL_TILT_DEG


def inter_row_shading(
    panel_slant_length_m: float,
    tilt_deg: float,
    *,
    latitude_deg: float | None = None,
    solar_altitude_deg: float | None = None,
) -> RowSpacing:
    """Compute shadow-free row spacing, Ground Coverage Ratio, and layout loss.

    Provide either ``latitude_deg`` (the sun altitude is then taken at
    winter-solstice solar noon) or an explicit ``solar_altitude_deg`` for a
    chosen design time.

    Geometry, with L the slant length of the row and the tilt angle beta:
      - vertical rise:            H = L * sin(beta)
      - ground footprint:         b = L * cos(beta)
      - shadow-free gap:          D = H / tan(sun altitude)
      - row pitch (base to base): P = b + D
      - Ground Coverage Ratio:    L / P
      - layout loss (area share): D / P   (the ground taken up by the gap)
    """
    if panel_slant_length_m <= 0:
        raise ValueError("panel_slant_length_m must be positive")
    if not 0 <= tilt_deg < 90:
        raise ValueError("tilt_deg must be in [0, 90)")

    if solar_altitude_deg is None:
        if latitude_deg is None:
            raise ValueError("provide either latitude_deg or solar_altitude_deg")
        solar_altitude_deg = winter_solstice_noon_altitude(latitude_deg)
    if not 0 < solar_altitude_deg < 90:
        raise ValueError(
            "solar altitude must be in (0, 90) degrees; at this latitude the "
            "winter-noon sun is too low — pass an explicit solar_altitude_deg "
            "for a less extreme design time"
        )

    beta = radians(tilt_deg)
    height = panel_slant_length_m * sin(beta)
    base = panel_slant_length_m * cos(beta)
    gap = height / tan(radians(solar_altitude_deg))
    pitch = base + gap
    gcr = panel_slant_length_m / pitch
    layout_loss = gap / pitch

    return RowSpacing(
        tilt_deg=tilt_deg,
        latitude_deg=latitude_deg,
        solar_altitude_deg=solar_altitude_deg,
        panel_slant_length_m=panel_slant_length_m,
        row_height_m=height,
        horizontal_base_m=base,
        inter_row_gap_m=gap,
        row_pitch_m=pitch,
        ground_coverage_ratio=gcr,
        layout_loss_fraction=layout_loss,
    )
