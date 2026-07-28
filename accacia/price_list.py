"""Module price list — per-brand/model rates with a 'last updated' stamp.

A small, persistable catalogue of module prices. Prices move constantly and are
the user's to maintain, so entries are seeded only with an *indicative* rate and
a reference date, and every entry carries a ``last_updated`` stamp so a stale
price is easy to spot. The web tool persists the user's edits in the browser and
stamps the date on each change; this module provides the seed defaults and the
staleness logic that mirror it, and lets the rest of the engine look a rate up.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from .brands import DEFAULT_MODULE_WP, INDICATIVE_MODULE_RATE_PER_WATT
from .vendors import VENDORS

# When the indicative reference rates below were set. Real edits (in the web
# tool or by calling code) should stamp the actual date.
SEED_DATE = date(2026, 1, 1)
DEFAULT_STALE_DAYS = 90


@dataclass
class PriceEntry:
    brand: str
    model: str
    wattage: int
    rate_per_watt: float          # module-only price, rupees per watt
    last_updated: date
    indicative: bool = False      # True = seeded placeholder, not a confirmed price

    def days_since_update(self, today: date | None = None) -> int:
        return ((today or date.today()) - self.last_updated).days

    def is_stale(self, max_age_days: int = DEFAULT_STALE_DAYS,
                 today: date | None = None) -> bool:
        """A price older than ``max_age_days`` (or still indicative) is stale."""
        return self.indicative or self.days_since_update(today) > max_age_days


def default_price_list() -> list[PriceEntry]:
    """Seed a price list from the Section 5 vendor roster — one entry per brand,
    at the indicative rate and reference date, flagged indicative until edited."""
    return [
        PriceEntry(
            brand=v.name,
            model=v.notable_model or "(model to confirm)",
            wattage=DEFAULT_MODULE_WP,
            rate_per_watt=INDICATIVE_MODULE_RATE_PER_WATT,
            last_updated=SEED_DATE,
            indicative=True,
        )
        for v in VENDORS
    ]


def find_entry(
    entries: list[PriceEntry], brand: str, model: str | None = None
) -> PriceEntry | None:
    """Find an entry by brand (and optional model), case-insensitively."""
    b = brand.strip().lower()
    m = model.strip().lower() if model else None
    for e in entries:
        if e.brand.lower() == b and (m is None or e.model.lower() == m):
            return e
    return None


def stale_entries(
    entries: list[PriceEntry], max_age_days: int = DEFAULT_STALE_DAYS,
    today: date | None = None,
) -> list[PriceEntry]:
    """Entries whose price is stale (indicative or older than the threshold)."""
    return [e for e in entries if e.is_stale(max_age_days, today)]
