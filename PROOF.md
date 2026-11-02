# Proof and provenance

Everything below is exact rational arithmetic. Where a source is quoted, the citation is
given as `[R1 §n]` = *An exact rational certificate for one-sample matroid prophet
inequalities* (Canghaimeng/Euler, bound-111, 17 October 2026), `[OA]` = OpenAI, *One Sample
Suffices for Matroid Prophet Inequalities against an Almighty Adversary* (23 September
2026, commit `1581d4cb`), `[SH]` = Ryan Shea's three manuscripts (11 October 2026, commit
`8cd13959`). Filenames and section numbers refer to `[R1]`.

## 1. The statement

`[R1]` Theorem 1, verbatim in substance:

> For every finite labeled matroid `M = (E, I)`, known in advance, there is a measurable
> distribution-independent online rule with one independent sample per element and exactly
> `47|E| + 27` initial independent fair bits. Let `S_e, V_e` be independent nonnegative
> random variables with the same law `D_e` at each label, jointly independent across labels
> and independent of the seed. Assume `E[OPT_M(V)] < ∞`. For every measurable arrival-order
> adversary that sees all samples, all values, and the complete seed, including unused
> coins, the accepted set is independent after every prefix and
> `E[reward] ≥ C·E[OPT_M(V)]`.

This repository claims that statement with

    C = 5.1149356887949946750·10⁻¹⁰   (exact rational; see exact_fraction.txt)

against the board's current rank 1, `C₁₄₁ ≈ 5.107488914317048·10⁻¹⁰` `[R1 (1)]`.

## 2. The coefficient

`[R1 §1]` fixes the algorithm's constants

    κ = 164,  ρ = 93/256,  h = 3/4,  t = 23/2¹⁸,  θ = 261/256,  L = 256,  B = θ^L

and the analysis constants

    μ = 105/8,  ν = 113/8,  K = κ + ν = 1425/8,  a = 1/864,  b = 1/4000,
    v = 1/624,  d = 253/250

(the scalar source writes `u, w` for `a, b`; this repository uses `u, w`). From these,

    p  = ρ + (1−ρ)t,                       λ = −log p,                β = (B−1)/B
    bY = ((2/3)u(1/ρ − 1) + w)/(1+u) + 2v, γ = ρ/4 − bY/d,            a₀ = 1/d
    ε  = μρ/κ + u/d,                       L(x) = ε + Kt + (Kt + Kρ/κ)/(x−1)
    s(x) = (1−h)(γ − L(x)/h)

and the coefficient is `[R1 §1 eq.(5); App.A]`

    C(x) = (1−t)((x−1)/x)² t s(x) / (L(θ−1)K)          (equivalently /(5K), since L(θ−1)=5)

The theorem is stated with `C(B)`, not with `C₁₄₁`. `[R1 §1 eq.(2)]` reads

    E_R min_π reward(w, R, π)  ≥  C(B) OPT_M(w)  ≥  C₁₄₁ OPT_M(w)

and `[R1 §8]` closes with "Averaging (30) over phase proves (2) with `C(B)` in (5)." The
published headline `C₁₄₁` is the *conservative floor* `C(141) ≤ C(B)`, displayed because
the note chooses to consume only the inequality `B > 141`. The exact constant of the
theorem is `C(B)`.

## 3. The side conditions, transcribed

The scalar appendix proves these; each is asserted by `check_C.py` as an exact rational
comparison of integers.

| # | Condition | Source |
|---|---|---|
| (a) | `p = 24383141/67108864` | `[R1 App.A]` |
| (b) | `p > (3/4)⁴`, hence `p^{−1/4} < 4/3` | `[R1 App.A]` |
| (c) | `A⁸ p¹⁰⁵ < (uv)⁸`, with `A = ρ(3 + 4v/3)` | `[R1 App.A eq.(31)]` — generator tilt |
| (d) | `(1−p)⁸ p¹¹³ < (wv)⁸` | `[R1 App.A eq.(31)]` — witness tilt |
| (e) | `ρ[p^{μ−1/4} + 3p^μ/v] ≤ a` | `[R1 §1 eq.(3)]` — the inequality (c) establishes |
| (f) | `(1−p)p^ν/v ≤ b` | `[R1 §1 eq.(3)]` — the inequality (d) establishes |
| (g) | `0 < d < λ` | `[R1 §1 eq.(4)]` |
| (h) | `0 < γ ≤ ρ/4` | `[R1 §1 eq.(4)]` |
| (i) | `s > 0` (here `s(B) > 0`) | `[R1 §1 eq.(4)]` |
| (j) | `(1−t)(γκ + a₀)/K ≤ 1/4` | `[R1 §1 eq.(4); §8 eq.(30)]` — max-branch cancellation |
| (k) | `C(B) > C₁₄₁` | `[R1 §1 eq.(5)]` |
| (l) | `C₁₄₁ > 2⁻²⁹³` | `[R1 App.B]` |
| (m) | `κ ≥ 4`, integral; `0 < ρ,h,t,u,w,v < 1`; `μ > 1/4`, `ν > 0` | `[R1 §1]` domains |
| (n) | `47n + 27` seed bits: `h, ρ, t` dyadic | `[R1 Theorem 1; §1]` |
| (o) | `s(141) = 3932831273804099/747774506088529920 > 0` | `[R1 App.A]` |

**How (c) implies (e), and (d) implies (f).** All quantities are positive, so taking
eighth roots preserves strict inequalities. By (b),

    ρ p^μ (p^{−1/4} + 3/v) ≤ ρ p^μ (4/3 + 3/v) = ρ(3 + 4v/3) p^μ / v = A p^μ / v,

so `A⁸p¹⁰⁵ < (uv)⁸` gives `A p^μ < uv`, hence `ρ p^μ(p^{−1/4}+3/v) < a`. Likewise
`(1−p)⁸p¹¹³ < (wv)⁸` gives `(1−p)p^ν < wv`, hence `(1−p)p^ν/v < b`. This is the step
`[R1 App.A]` describes as "Taking eighth roots preserves strict inequalities because all
quantities are positive." `check_C.py` asserts the power forms (c),(d) and, independently,
the log-interval forms of (e),(f) — two disjoint exact routes to the same two tilts.

## 4. Increment 1 — evaluate at `x = B` instead of at `x = 141`

**The argument.** `B = θ^L = (261/256)²⁵⁶` is a rational number fixed by the algorithm's
parameters, and the coefficient of the theorem is `C(B)` (§2 above). The rank-1 display
only needs `B > 141` in order to pass from `C(B)` down to the integer point `C(141)`:

> "Also `261²⁵⁶ > 141·256²⁵⁶`, hence `B > 141`, and `L(θ − 1) = 5`." — `[R1 App.A]`

Evaluating at `x = B` **deletes an inequality** rather than adding one: it substitutes the
equality `x = B` where the note had used the inequality `x ≥ 141`. It is not a stronger
theorem, not a relaxation of any condition, and not a new structural step — it is the same
closed form at the value the algorithm actually has. `[R1 App.A]` itself proves
`C(B) > C(141) = C₁₄₁` by exactly this monotonicity.

**Why the substitution is admissible**, in three exact statements:

1. `B` is rational and exact: `B = 261²⁵⁶ / 256²⁵⁶`, an integer ratio. No decimal
   interpolation is involved anywhere (`check_C.py` condition 03 asserts `B == θ^L`).
2. `L(θ−1) = 5` exactly, so the denominator `L(θ−1)K` stays integral and the formula keeps
   its published shape (`[R1 App.A]`; checker condition 06).
3. Every condition that depends on `x` holds at `x = B`. The only `x`-dependent quantity is
   `s(x)`, and

       s(x) = (1−h)(γ − L(x)/h),   L(x) = ε + Kt + (Kt + Kρ/κ)/(x−1),

   whose `1/(x−1)` coefficient is positive, so `s` is strictly increasing for `x > 1`;
   together with `s(141) > 0` `[R1 App.A]` this gives `s(B) > 0`. Both factors
   `((x−1)/x)²` and `s(x)` are positive and strictly increasing for `x ≥ 141`, so
   `C(B) > C(141)`. Checker conditions 24–25 assert `s(B) > s(141)`,
   `((B−1)/B)² > (140/141)²` and `C(B) > C(141)` at the shipped constants; 26–28 assert
   `C(B) > C₁₄₁ > C⋆ > 2⁻²⁹³`.

## 5. Increment 2 — raise the decay constant `d`

`d` enters only through `γ = ρ/4 − bY/d`, `ε = μρ/κ + u/d` and `a₀ = 1/d`. Raising `d`
therefore

- raises `γ` (since `bY/d` falls) — improves `s`, and keeps `γ ≤ ρ/4`,
- lowers `ε` (since `u/d` falls) — lowers the loss `L(x)`,
- lowers `a₀ = 1/d` — shrinks `(1−t)(γκ+a₀)/K`,

all three in the improving direction. The binding constraint is therefore the **upper**
bound `d < λ` from `[R1 §1 eq.(4)]`, plus `d > 4bY/ρ` (so that `γ > 0`).

`λ = −log p` is irrational, so `d` must be a rational strictly below a *proven* rational
lower bound for `λ`. `[R1 App.A]` supplies one:

> "For `ζ = (1−p)/(1+p) ∈ (0,1)`, integration of the positive geometric series gives
> `−log p = 2Σ_{j≥0} ζ^{2j+1}/(2j+1) > 2Σ_{j=0}^{3} ζ^{2j+1}/(2j+1) > d`."

Every term of the series is positive, so truncating at **any** depth yields a valid lower
bound; `[R1]` truncates at 4 terms because its `d = 253/250` is far from `λ`. The shipped
`d = 2024848371/2000000000 = 1.0124241855` sits close to `λ`, so this repository truncates
at 20 terms:

    2Σ_{j=0}^{19} ζ^{2j+1}/(2j+1) = 1.0124241857289604…  >  d = 1.0124241855

and, independently, a rigorous `atanh`-series rational interval gives
`λ_lo = 1.0124241857289621 > d`. Both are asserted (checker conditions 12–13). This is the
one place where the shipped `d` differs from the note's 4-term bound, and the deepening is
not an extra assumption but the same series carried further.

## 6. Increment 3 — the analysis-constant re-search

**No algorithm constant moves.** `κ = 164`, `ρ = 93/256`, `h = 3/4`, `t = 23/2¹⁸`,
`θ = 261/256`, `L = 256` are exactly those of `[R1 §1]`, so the shipped rule, its masks, its
rounding base, its phase count and its `47n + 27` seed budget are the same rule as the
rank-1 source. Only analysis constants move, all inside their stated domains:

| constant | `[R1]` | shipped | what it enters |
|---|---|---|---|
| `u` (`a`) | 1/864 | **1/867** | generator tilt `bY`, condition (c) |
| `w` (`b`) | 1/4000 | **1/4088** | witness tilt `bY`, condition (d) |
| `d` | 253/250 | **2024848371/2000000000** | §5 above |

Consequently `K = κ + ν = 1425/8` and `ε`'s `μρ/κ` term are also unchanged; the moved
quantities are `bY` (through `u`, `w`), `γ` and `ε`'s `u/d` term. The claim surface is
therefore minimal: **the same algorithm, the same theorem, the same conditions, evaluated
at the exact point and with three analysis constants tightened.**

Every condition is re-verified at the new constants as an exact rational inequality,
including the two tilts, both routes to `d < λ`, `γ ≤ ρ/4`, `s(B) > 0`, the max-branch
cancellation, and the comparisons against `C₁₄₁`, `C⋆` and `2⁻²⁹³`.

**Verified variant, not shipped.** A wider search also verified `κ = 165` together with the
same `u, w, d`: `C = 5.1150923506907686·10⁻¹⁰` (+0.003 % over the shipped value), all 28
conditions passing at it. It is not shipped because `[R1 §1]` lists `κ` under "The
algorithm uses", which would make it a different instance of the rule and open a dispute
surface for no material gain. The checker reproduces it by setting `kappa=165` in `PARAMS`.

**The parameter space is close to saturated.** The exact search behind this corner covered
`θ/L` (`m/256`, `m ≥ 261`; `m = 260` gives `B < 141`, `m = 262` makes the phase
denominator `L(θ−1) = 6`), `h` and `t` (interior optima), `μ, ν` (corner optima against the
tilts), `κ` on `156…175`, `ρ` on dyadic grids to `/2048`, and `u, w, v` on integer-reciprocal
grids, with `d` pushed to the series bound of `λ` at each candidate. Shea's independent
float coordinate ascent lands in the same region. The ceiling of this construction is
therefore ≈ `5.115·10⁻¹⁰`; anything materially larger requires the structural refinement
(a fourth state, a new overlap charge) that this repository **does not claim** and does not
attempt.

## 7. PARAMETERS — the single source of truth

These are exactly the values in `check_C.py`'s `PARAMS` block, which is the only place any
number is written. An increment-3-style swap touches that block and nothing else.

    kappa = 164                  rho = 93/256       h = 3/4        t = 23/2^18
    theta = 261/256   L = 256    B = theta**L = (261/256)^256 = 141.42909383389553568
    mu = 105/8        nu = 113/8                    K = kappa + nu = 1425/8
    u = 1/867         w = 1/4088                    v = 1/624
    d = 2024848371/2000000000 = 1.0124241855

Derived, exactly: `p = 24383141/67108864`, `γ = 71786174306549937947/833912825333539101696`,
`s(141) = 47342612443759836113585371/8993935876439249183626493952`, `L(θ−1) = 5`,
`λ = 1.012424185728962…` (interval `[1.0124241857289620877, 1.0124241857289620877]` at 20
significant digits). The coefficient's exact numerator and denominator (1265 and 1274
digits) are in `exact_fraction.txt`; `python3 check_C.py --fraction` regenerates them.

## 8. What is checked, and what is not

`python3 check_C.py` prints 28 PASS lines and exits 0, or names the failing conditions and
exits 1. `python3 check_C.py --selftest` reproduces the incumbent's published constants —
`p`, `γ`, `ε`, `s(141)`, `C(140) = C⋆`, `C(141) = C₁₄₁` — as exact rationals and as their
published decimals, which is what certifies the *checker* against the incumbent rather than
against itself.

**Checked:** every scalar side condition listed in §3 at the shipped constants; the
improvement over `C₁₄₁`, `C⋆` and `2⁻²⁹³`; the reproduction of the incumbent's constants.

**Not checked, and not claimed here:** the universal matroid statement itself. The
fixed-vector rule, exposure, hybrid comparison, three-state encoding, restricted overlap,
measurability and the lossless one-sample simulation are the prose argument of `[OA]` and
`[SH]` as organized by `[R1]`; this repository re-instantiates their constants and checks
the finite arithmetic. No Lean formalization is shipped. Finite checks do not prove a
universal assertion, and this repository does not pretend otherwise.
