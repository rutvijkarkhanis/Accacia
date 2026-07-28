"""Section 5 Vendor shortlisting — PVEL 2026 standing of Indian manufacturers.

Encodes the vendor table and the "diligence question that actually separates
vendors" from ``sections/05-certification-tiers.md``. Metrics that the KB does
not quantify for a vendor are left as ``None`` (breadth-listed vendors), rather
than guessed.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Vendor:
    name: str
    designations: int | None          # PVEL categories passed, out of 8
    avg_per_model: float | None       # average designations per model
    models_on_list: int | None        # number of models on the PVEL list
    years_top_performer: int | None
    notable_model: str | None
    note: str | None = None

    def score(self) -> tuple:
        """Sort key: more designations, then higher per-model average, then
        more consecutive years. ``None`` sorts last."""
        d = self.designations if self.designations is not None else -1
        a = self.avg_per_model if self.avg_per_model is not None else -1.0
        y = self.years_top_performer if self.years_top_performer is not None else -1
        return (d, a, y)


# PVEL 2026 standing (Section 5). Detailed metrics are populated where the KB states
# them; breadth-listed vendors carry name-only entries.
VENDORS: list[Vendor] = [
    Vendor("Adani Solar", 7, 6.5, None, 7, "ASB-M10-144-AAA",
           "Highest per-model average; 7 consecutive years Top Performer"),
    Vendor("ReNew", 7, None, None, None, None),
    Vendor("RenewSys", 7, 5.75, None, None, "DESERV EXTREME"),
    Vendor("Waaree", None, 3.13, 23, 5, None,
           "Largest roster (breadth over concentration); 5th consecutive year"),
    Vendor("Grew Solar", None, None, None, None, None),
    Vendor("EMMVEE", None, None, None, None, None),
    Vendor("Goldi Solar", None, None, None, None, None),
    Vendor("Avaada Electro", None, None, None, None, None),
    Vendor("Gautam Solar", None, None, None, None, None),
    Vendor("Rayzon Solar", None, None, None, None, None),
    Vendor("Vikram Solar", None, None, None, None, None),
    Vendor("Solex", None, None, None, None, None),
    Vendor("Tata Power Solar", None, None, None, None, None),
]

# Section 5 — the question that actually separates vendors at diligence.
DILIGENCE_QUESTION = (
    "Not 'is it certified' but: which IEC edition, does it include MQT21 (PID), "
    "and can you show the exact model's PVEL category breakdown + EL images for "
    "this specific batch?"
)


def shortlist_vendors(
    *,
    min_designations: int | None = None,
    require_metrics: bool = False,
) -> list[Vendor]:
    """Return vendors ranked by PVEL standing (best first).

    ``min_designations`` filters to vendors with at least that many PVEL
    designations (excludes name-only entries). ``require_metrics`` keeps only
    vendors with quantified standing.
    """
    result = list(VENDORS)
    if min_designations is not None:
        result = [
            v for v in result
            if v.designations is not None and v.designations >= min_designations
        ]
    if require_metrics:
        result = [v for v in result if v.designations is not None]
    return sorted(result, key=lambda v: v.score(), reverse=True)


def recommend_vendors(top_n: int = 3) -> list[Vendor]:
    """Top ``top_n`` vendors with quantified PVEL standing, best first."""
    return shortlist_vendors(require_metrics=True)[:top_n]
