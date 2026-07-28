"""Command-line enquiry-to-quote tool.

Usage::

    python -m accacia --area 20000 --location Ahmedabad --load 250 \
        --climate hot --payback-focused

    python -m accacia --area 20000 --psh 5.55 --json
"""

from __future__ import annotations

import argparse
import json
import sys

from .quote import Enquiry, build_quote
from .specs import SiteConditions


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="accacia",
        description="Solar EPC enquiry-to-quote engine (C&I rooftop, India 2026).",
    )
    # Section 1 site inputs
    p.add_argument("--area", type=float, required=True, help="Roof/land area (sqft)")
    p.add_argument("--location", help="City/state (resolves PSH), e.g. Ahmedabad")
    p.add_argument("--psh", type=float, help="Explicit Peak Sun Hours (overrides location)")
    p.add_argument("--pr", type=float, default=0.80, help="Performance ratio (default 0.80)")
    p.add_argument("--load", type=float, dest="load_kva",
                   help="Sanctioned load / contract demand (kVA)")
    p.add_argument("--shading-loss", type=float, default=0.08,
                   help="Shading/layout loss fraction (default 0.08)")
    p.add_argument("--area-per-kwp", type=float, default=100.0,
                   help="sqft per kWp (default 100)")
    p.add_argument("--capacity", type=float, dest="capacity_override",
                   help="Override feasible capacity (kWp)")

    # Mounting (tilted mounts derive the area derate from inter-row spacing)
    p.add_argument("--mount", choices=["flush", "tilted"], default="flush",
                   dest="mount_type", help="Mounting type (default flush)")
    p.add_argument("--tilt", type=float, dest="tilt_deg",
                   help="Tilt angle in degrees (tilted mount; default = latitude)")
    p.add_argument("--latitude", type=float, dest="latitude_deg",
                   help="Site latitude in degrees (tilted mount; default from location)")
    p.add_argument("--panel-length", type=float, dest="panel_slant_length_m",
                   default=2.3, help="Panel along-slope length in metres (default 2.3)")

    # Section 2 spec conditions
    p.add_argument("--climate", choices=["hot", "moderate", "cool"], default="moderate")
    p.add_argument("--reflective-mount", action="store_true",
                   help="Elevated/ground mount over a reflective surface")
    p.add_argument("--space-constrained", action="store_true",
                   help="Roof space is the binding constraint")
    p.add_argument("--aesthetic", action="store_true",
                   help="Aesthetic-sensitive facade / BIPV")
    p.add_argument("--long-hold", action="store_true",
                   help="Client holds the plant 20–25 yrs")
    p.add_argument("--payback-focused", action="store_true",
                   help="5–8 yr payback-focused C&I buyer")
    p.add_argument("--budget-sensitive", action="store_true")

    # Section 3 finance overrides
    p.add_argument("--cost-per-watt", type=float, help="₹/W turnkey (default 40)")
    p.add_argument("--grid-tariff", type=float, help="₹/unit commercial (default 8.5)")
    p.add_argument("--tariff-escalation", type=float, help="fraction/yr (default 0.04)")
    p.add_argument("--tenure", type=int, dest="tenure_years", help="years (default 25)")
    p.add_argument("--discount-rate", type=float, help="fraction (default 0.10)")

    # Module brand and rates
    p.add_argument("--brand", help="Module brand from the roster, e.g. 'Adani Solar'")
    p.add_argument("--module-rate", type=float, dest="module_rate_per_watt",
                   help="Module price in ₹/W (overrides the brand's indicative rate)")
    p.add_argument("--bos-rate", type=float, dest="bos_rate_per_watt", default=17.0,
                   help="Balance-of-system rate in ₹/W (default 17)")

    # Section 6 BOQ overrides
    p.add_argument("--module-wp", type=int, help="Module wattage (default 580)")
    p.add_argument("--inverter-kw", type=float, help="Inverter unit size kW (default 100)")
    p.add_argument("--dc-ac-ratio", type=float, help="DC:AC ratio (default 1.2)")

    p.add_argument("--json", action="store_true", help="Emit full quote as JSON")
    p.add_argument("--schedule", action="store_true",
                   help="Print the year-by-year cashflow schedule")
    p.add_argument("--boq", action="store_true",
                   help="Print the full bill of quantities with per-line specs")
    return p


def _finance_overrides(args: argparse.Namespace) -> dict:
    keys = ("cost_per_watt", "grid_tariff", "tariff_escalation",
            "tenure_years", "discount_rate")
    return {k: getattr(args, k) for k in keys if getattr(args, k) is not None}


def _boq_overrides(args: argparse.Namespace) -> dict:
    keys = ("module_wp", "inverter_kw", "dc_ac_ratio")
    return {k: getattr(args, k) for k in keys if getattr(args, k) is not None}


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)

    if args.location is None and args.psh is None:
        print("error: provide --location or --psh", file=sys.stderr)
        return 2

    enquiry = Enquiry(
        site_area_sqft=args.area,
        location=args.location,
        psh=args.psh,
        pr=args.pr,
        sanctioned_load_kva=args.load_kva,
        shading_loss=args.shading_loss,
        area_per_kwp=args.area_per_kwp,
        capacity_override_kwp=args.capacity_override,
        mount_type=args.mount_type,
        tilt_deg=args.tilt_deg,
        latitude_deg=args.latitude_deg,
        panel_slant_length_m=args.panel_slant_length_m,
        brand=args.brand,
        module_rate_per_watt=args.module_rate_per_watt,
        bos_rate_per_watt=args.bos_rate_per_watt,
        conditions=SiteConditions(
            climate=args.climate,
            reflective_ground_mount=args.reflective_mount,
            space_constrained=args.space_constrained,
            aesthetic_sensitive=args.aesthetic,
            long_hold=args.long_hold,
            payback_focused=args.payback_focused,
            budget_sensitive=args.budget_sensitive,
        ),
        finance_overrides=_finance_overrides(args),
        boq_overrides=_boq_overrides(args),
    )

    try:
        quote = build_quote(enquiry)
    except (ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(quote.to_dict(), indent=2, default=str))
        return 0

    print(quote.summary())
    if args.schedule:
        print("\n=== SCHEDULE (year | gen | CAPEX cum | RESCO cum) ===")
        for r in quote.finance.rows:
            print(
                f"  {r.year:>2}  {r.generation_units:>12,.0f}  "
                f"{r.capex_cumulative:>16,.0f}  {r.resco_cumulative:>16,.0f}"
            )
    if args.boq:
        print("\n=== BOQ DETAIL (item | spec | qty | cost) ===")
        for ln in quote.boq.lines:
            qty = f"{ln.quantity:g} {ln.unit}" if ln.quantity and ln.unit else "lump"
            print(f"  {ln.item}\n    {ln.spec}\n    {qty:<12} ₹{ln.cost:,.0f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
