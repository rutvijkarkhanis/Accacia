"""Module brand catalogue for pricing the Bill of Quantities module line.

Brands and their PVEL 2026 standing come from Section 5 (``accacia.vendors``).
Module PRICES are deliberately NOT fixed here: module rates move constantly and
are negotiated per order, so each brand carries only an *indicative* module rate
(rupees per watt) meant to prime the field — the user is expected to override it
with a current, negotiated figure. All brands share the same indicative default
rather than inventing per-brand price differences the knowledge bank cannot
support; the brand choice conveys PVEL standing and wattage, and the rate is the
user's to set.
"""

from __future__ import annotations

from dataclasses import dataclass

from .vendors import VENDORS

# Indicative module-only price in rupees per watt (module, not turnkey). A
# placeholder midpoint to prime the input — always confirm and override with a
# live quote. Paired with a default balance-of-system rate of ~17 it reproduces
# the tool's default turnkey cost of about 40 rupees per watt.
INDICATIVE_MODULE_RATE_PER_WATT = 23.0
DEFAULT_MODULE_WP = 580


@dataclass
class Brand:
    name: str
    pvel_designations: int | None      # PVEL categories passed, out of 8 (None = roster-listed)
    default_wp: int
    indicative_rate_per_watt: float
    note: str | None = None

    def tier(self) -> str:
        """A short PVEL-standing label for the quotation module line."""
        if self.pvel_designations is None:
            return "PVEL Top Performer roster"
        return f"{self.pvel_designations}/8 PVEL designations"


# Built from the Section 5 vendor roster so the two never drift apart.
BRANDS: list[Brand] = [
    Brand(v.name, v.designations, DEFAULT_MODULE_WP,
          INDICATIVE_MODULE_RATE_PER_WATT, v.note)
    for v in VENDORS
]


def brand_names() -> list[str]:
    """Brand names in roster order (best PVEL standing first)."""
    return [b.name for b in BRANDS]


def get_brand(name: str) -> Brand:
    """Return the catalogue entry for a brand name (case-insensitive)."""
    key = name.strip().lower()
    for b in BRANDS:
        if b.name.lower() == key:
            return b
    raise KeyError(f"unknown brand {name!r}; see brand_names()")
