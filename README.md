> **Superseded 2026-11-02** by [darkhipo/matroid-prophet-tight-corner](https://github.com/darkhipo/matroid-prophet-tight-corner) (exact-B evaluation + d/u/w corner re-search; C = 5.1149356887949946750e-10, 28/28 exact conditions).
>
> **Erratum:** below, `B = (261/256)^256` displays as ≈ 142.9; the correct value is **141.42909383389553568**. The exact-rational claims and checker in this repo are unaffected.

# Matroid prophet inequality: the exact constant C(B)

For every finite matroid, against the same almighty full-seed arrival-order
adversary, with one sample per element and seed budget 47|E|+27 bits, the
guaranteed fraction of the expected offline optimum is

$$C(B) = 5.1106085087308568\cdot 10^{-10},\qquad B=\left(\tfrac{261}{256}\right)^{256}\approx 142.9,$$

where C(B) is the closed form (5) of the bound-111 paper evaluated at the
rational $x=B$ in exact arithmetic. The exact numerator/denominator pair
(≈1900 digits each) is emitted by the certificate and stored verbatim in
[`exact_fraction.txt`](exact_fraction.txt) and [`result.json`](result.json).

This **exceeds the current listed value** $C_{141}\approx 5.1074889\cdot10^{-10}$
(bound-111 of `canghaimeng/openai-math-improvement`) by $6.108\cdot10^{-4}$
relative — and the bound-111 paper itself proves the theorem with exactly this
$C(B)$: *"Averaging (30) over phase proves (2) with $C(B)$… $C(B) > C(141) = C_{141}$."*
The listed value is the theorem's constant floored to the integer 141; this
repository evaluates the same closed form at the rational $x=B$ in exact
arithmetic. Nothing structural is new.

## What is whose

- **OpenAI** (One-Sample-Suffices preprint, commit `1581d4cb`): the
  construction (κ=164, ρ=93/256, h=3/4, t=23/2¹⁸, θ=261/256, L=256) and the
  structural prophet-inequality argument.
- **Ryan Shea** (`shea256/matroid-prophet-inequality`, commit `8cd13959`): the
  analysis constants (a, b, v, d, μ, ν), the scalar chain, and the earlier
  certificate C⋆.
- **Qiuyu Chen (Euler)** (`canghaimeng/openai-math-improvement`, bound-111):
  the conservative evaluation B > 141 (the current listed record), the exact
  scalar checker this file extends, and the paper's own statement that C(B)
  is larger.
- **MultiAgency / darkhipo** (this repository): the exact evaluation at
  x = B — one rational substitution in the published closed form — plus this
  certificate file. That is the entire contribution.

## The certificate

`check_scalar_B.py` (a derivative of bound-111's embedded `check_scalar.py`;
its supplement ZIP lives inside `paper.pdf`'s embedded-file streams) performs
19 exact-rational checks: every x-independent upstream check verbatim
(tilts, log lower bound, γ, ε, phase denominator, C₁₄₁ byte-exact
reproduction), plus the new ones (B exact, s(B) > 0, monotone gains,
C(B) > C₁₄₁ > C⋆). Runs in seconds with stdlib `fractions` only:

    python3 check_scalar_B.py

**Evidence level: arithmetic certificate on an inherited, unformalized
structural proof.** The scalar layer is exactly checked; the structure
(fixed-vector rule, exposure, hybrids, measurability) remains the prose of
the cited papers — as it does for every current row of this lane, none of
which carries Lean.

---

## Why this repo is up

Public evidence, honestly superseded: the exact-B evaluation stands with its erratum corrected, and the repo records being superseded by matroid-prophet-tight-corner — kept as the reproducible exact-arithmetic record.

[BigO-Hunter](https://github.com/BigO-Hunter) is the darkhipo swarm's tracking & packaging org for contributions toward [Big O Speedrun](https://bigospeedrun.com) — a companion, never the project. Org story: [profile](https://github.com/BigO-Hunter/.github) · [bigo-hunter.github.io](https://bigo-hunter.github.io).

## What work can be done here

Complete as a record — the exact-B evaluation stands with its erratum corrected, and the repo records its supersession by matroid-prophet-tight-corner. Open work: none pending; kept for the erratum audit trail and exact-arithmetic reproducibility.

## License

Licensed under the Copy-Free/Stays-Free (CFSF) License — see [LICENSE](LICENSE) ([github.com/darkhipo/cfsf](https://github.com/darkhipo/cfsf)). CFSF: copy-free (use for any purpose) and stays-free (nobody may fence this work). The name is unclaimed in software licensing (checked 2026-11-09) and is deliberately not "Copyfree" — the Copyfree Initiative's certification mark — since CFSF's anti-enclosure condition is excluded by their standard. 
