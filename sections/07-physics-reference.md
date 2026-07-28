# 7. Physics Reference (for explaining *why*, not just *what*)

[← Back to index](../README.md)

- **P-n junction / depletion region** — diffusion of carriers across doped silicon leaves fixed ionized atoms behind, creating a permanent built-in electric field that separates photon-generated electron-hole pairs before they recombine
- **Bandgap (silicon ~1.1 eV)** — minimum photon energy needed to free an electron; below-bandgap photons pass through unabsorbed (why tandem cells stack a second material)
- **Contact recombination** — the main loss PERC never solved; TOPCon fixes it with an ultra-thin tunnel oxide (quantum tunneling lets carriers through) + a doped polysilicon selective contact layer
- **Temperature coefficient** — physical basis for why HJT/hot-climate matching matters
- **PID mechanism** — stray leakage voltage across the module frame/encapsulation gradually disturbs the same junction field, causing slow output decline — this is why MQT21 exists

> These mechanisms justify the spec calls in [Section 2 Product/Spec Selection](./02-product-spec-selection.md) and the test tiers in [Section 5 Certification & Differentiation Tiers](./05-certification-tiers.md).
