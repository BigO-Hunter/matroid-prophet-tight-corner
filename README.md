# Matroid prophet inequality: an exact rational guarantee above the listed C₁₄₁

**The claim.** For every finite matroid, against the almighty full-seed arrival-order
adversary, with one independent sample per element and `47|E|+27` fair initial bits, the
online rule of the construction below satisfies

    E[reward]  ≥  C · E[OPT_M(V)]

where **C is the exact rational**

<details>
<summary><b>C = (1−t)((B−1)/B)² t s(B) / (L(θ−1)K) — click for the canonical numerator/denominator (1265 and 1274 digits)</b></summary>

    numerator   = 10711566875369673025817739975675683817681254647571931425832334543063741170487901347395115110979677217020110072027224001407975565682479910379064056051856110587552968297518335842443347228863032247480602033311115141178361962049930427471348278936546140962979677505107556860879842625017607117647304875913843463520436638857372516634611042953530030081011846949529992191076964942957562225464407420723613556271554288186302293739154203364480688727396143212442722941403154685033052698598076220879459542755819539438096974306217396593328748039381450326567871835981552289724106589863123790770777691815071281816363974113183832334136528047280852714643420118982639437098849678077760734832565564941254722648053013856764048783001245283800450921477388825905616538985551590108856651151654539035931295539713436774459927303619975247412070497885176222467986008637284380136414903853552935373830077436231194418285196207655567608345999924993438960913102048581554538701288808176134159156918819497819144546729725752185358701104045251865776142185921617414805205600431946901613126683972200086303736937211036397777914394362644325240215146572060964568180304900821182021099713302171647737934530510943118482302623365469152759390293246603580095177293153273183535467641160806826282382126779104320960897
    denominator = 20941743019046959339210034877497733472902770324015817916202532402733739323035274822665208186318560410490808710130756157802688824657663993990528360769508586137134305559717112104810922947706477204165208638772582951574012424152075236800349148901748044915808498180145331418771734517320643280965070123893094436697963820154979173076373139474611498747277690428440124920406425058373509365439422794808328824604932318992559915808460143622373979075557155344151195417701839415151781952181375047355843263370014316184010851721921256426450178091798365897182090674223975547562233247970963630088696205985397960849370106576455810337721343162816940252840355533811187592681553146449459309876768945111117334174151995283867201943373324170415916027520299574753733372214756739731807661398926466223370725873385867122419682412668485047541608859099742992745804264177752494154620396127630406084392823292316264970286291043828407027458902082401480856367435813052140163420372917870397779365590934442000575370384598392194228597130479430306181377139345328145806232711329250860384652897661895123276803341156639481653109881391115926777969325455371657816938224906926576769518563519594427312540762536561834223382428073012610138133940355625475278038662799240966501339831244699878977436291690956725090489896796160

</details>

and, in 20 significant digits,

    C = 5.1149356887949946750e-10.

This is **+0.145801 %** above the value currently listed at rank 1 of the board,
`C₁₄₁ = 165971304277649481670619/324956758716416046811841770291200 ≈ 5.107488914317048·10⁻¹⁰`.

The exact integers above are the authority; every decimal in this repository is display
only. `exact_fraction.txt` carries the same pair verbatim, and `check_C.py` regenerates it.

## The board and the route it is filed under

Board: <https://bigospeedrun.com/other/matroid-prophet> — quantity is the largest
guaranteed fraction `C` with `E[reward] ≥ C·E[OPT]`, one sample per element of an
arbitrary finite matroid, adversary sees all samples, all values and all seed bits;
higher wins.

The route and evidence rules, as recorded in the campaign's board recon
(`/about#submit`, `/about#latest-results`, `llms.txt`; the live pages were not re-fetched
at package time):

> "publish a public GitHub repo stating exact value + conditions verbatim + written proof
> + exact checker; bigospeedrun's hourly agent flags it, a second agent reads it, checks
> same-problem, adds as *'Claimed'* if new best."

> "Standard = same problem, higher exact bound."

So this repository is the artifact, and the reachable row is **Claimed** — the same row
the current rank 1 occupies. There is no Lean challenge, no prove2me campaign and no
review repository for this problem; the verifier has no matroid-prophet statement.

## What is whose

- **OpenAI** — *One Sample Suffices for Matroid Prophet Inequalities against an Almighty
  Adversary*, OpenAI Math release preprint, 23 September 2026, pinned commit
  `1581d4cbdd69a0faf34b2089614fe2a814316a6a`: the construction (density paths, canonical
  generator budget, fixed-vector model, one-sample simulation) and the internal
  fixed-vector bound `2⁻²⁹³`.
- **Ryan Shea** — *The fixed-vector rule and its statistics*, *Sharper one-sample matroid
  prophet inequalities*, *Three-state generator encoding and restricted overlap*,
  11 October 2026, pinned commit `8cd1395994596d89ad20c2af8b69dab8e3402ee1`,
  <https://github.com/shea256/open-math-problems>: the analysis constants, the scalar
  chain, and the earlier certificate `C⋆`.
- **Qiuyu Chen (Euler)** — *An exact rational certificate for one-sample matroid prophet
  inequalities*, bound-111 of
  <https://github.com/canghaimeng/openai-math-improvement>, 17 October 2026: **the rank-1
  source this repository builds on** — the exact scalar certificate, the closed form
  `C(B)`, the conservative evaluation `B > 141`, and the paper's own statement
  `C(B) > C(141) = C₁₄₁`.
- **darkhipo (this repository)** — the evaluation of that published closed form at the
  *exact* rational `x = B = (261/256)²⁵⁶` instead of the floored integer `x = 141`, a
  refinement of the decay constant `d`, refinement of the two tilt constants `u` and `w`,
  and the certificate file below. Nothing structural is new: no new inequality, no new
  algorithm, the same `47n+27` seed budget.

## Prior publication

`darkhipo/matroid-prophet-exact-B` (public since 2026-11-02T06:52Z) published
**Increment 1 alone** — the same closed form evaluated at `x = B`, `C(B) =
5.1106085087308568·10⁻¹⁰`. This repository supersedes it: strictly higher at
`5.1149356887949947·10⁻¹⁰` (+0.084671 % over that figure), same construction family, every
condition re-verified at the constants shipped here. The earlier repository's README
displays `B ≈ 142.9`, a typo for `B = 141.42909383389553568`; the erratum is being filed
separately and nothing in this repository depends on that display.

## The certificate

`check_C.py` is stdlib-only (`fractions`, `decimal`; no NumPy, no floats in any claim),
runs in about a second, and asserts **28 exact rational conditions** — the full side
condition list of the source, each with a citation comment, plus the comparisons against
the incumbent, `C⋆` and `2⁻²⁹³`:

    python3 check_C.py              # full certificate; exit 0 = all conditions hold
    python3 check_C.py --selftest   # reproduce the incumbent's published constants exactly
    python3 check_C.py --fraction   # emit the numerator/denominator

`--selftest` is the part that certifies the checker rather than the claim: at the
bound-111 parameter set the same code path must reproduce, as exact rationals,
`p = 24383141/67108864`, `γ = 69959099203/812800834560`,
`ε = 69328715/2294341632`, `s(141) = 3932831273804099/747774506088529920`,
`C(140) = C⋆` and `C(141) = C₁₄₁` digit for digit, and their published decimals. It does.

Exit status is `0` when every condition holds and `1` when one fails, with each failing
condition named on stderr. `PROOF.md` carries the derivation and transcribes every
condition with its source section.

## Method, in one paragraph

The source's coefficient is a closed form in a variable `x`, `C(x) = (1−t)((x−1)/x)² t
s(x)/(5K)`, and the constant it displays is `C(141)` — the value at the *integer* `141`,
chosen only because `B = θ^L = (261/256)²⁵⁶ ≈ 141.429` is proved to exceed it. Since `C`
is strictly increasing for `x ≥ 141` (both factors increase and `s(x)` has a positive
`1/(x−1)` coefficient), the published `B > 141` is an inequality the theorem does not
need: `B` is itself a rational fixed by the algorithm's parameters, so the same closed
form can be evaluated at `x = B` exactly, replacing an inequality by an equality. That is
Increment 1. Increment 2 pushes the decay constant `d` from `253/250` up to just below
`λ = −ln p` (the only binding constraint on it), which raises `γ`, lowers `ε` and lowers
`a₀` simultaneously; `d` must be rational and provably below the irrational `λ`, so a
positive-term `ζ`-series truncation at 20 terms supplies a rigorous rational lower bound —
any truncation depth is valid because every term is positive. Increment 3 re-searches the
two tilt constants of the same construction, `u` and `w`, inside their stated domains and
re-verifies every condition exactly. **No algorithm constant moves**: `κ, ρ, h, t, θ, L`
are identical to the rank-1 source, so the rule, its masks, its phase count and its
`47n+27` seed budget are unchanged — the entire improvement lives in the evaluation
point and in three analysis constants. Every inequality in this repository is an exact
rational comparison of integers — `A⁸p¹⁰⁵ < (uv)⁸`, `(1−p)⁸p¹¹³ < (wv)⁸`, `261²⁵⁶ >
141·256²⁵⁶`, `d < λ_lo` — never a floating-point or logarithm evaluation.

## Scope — what is and is not claimed

**Claimed:** an exact-rational certificate for this construction under the source's stated
model and conditions, with every side condition checked as an exact rational inequality.
The universal statement (that the rule is prefix-feasible and reaches `C·OPT` for every
finite matroid) is the cited papers' argument, re-instantiated at these constants; this
repository does not re-prove it and ships no formalization.

**Not claimed:** no new structural inequality; no new algorithm; no Lean proof; no
polynomial-time or practical-performance claim; no exhaustive novelty claim. The
parameter space of this construction is close to saturated — see `PROOF.md` §6 — so
materially larger constants would need the structural refinement this repository
explicitly does not attempt.

**Evidence level:** an arithmetic certificate on an inherited, unformalized structural
proof — the same level as every current row of this lane, none of which carries Lean.
