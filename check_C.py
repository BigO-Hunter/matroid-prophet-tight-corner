#!/usr/bin/env python3
"""Exact-rational certificate checker for the one-sample matroid-prophet constant.

Recomputes the shipped coefficient C from the exact parameter set (stdlib
`fractions` only, no floating point anywhere in a claim) and asserts EVERY side
condition of the source proof as an exact rational inequality.  Each assertion
carries a citation to the source it is transcribed from:

  [R1]  "An exact rational certificate for one-sample matroid prophet
        inequalities", Canghaimeng/Euler, bound-111, October 17 2026
        (paper PDF in this repository's reference list; sections cited below).
  [OA]  OpenAI, "One Sample Suffices for Matroid Prophet Inequalities against an
        Almighty Adversary", September 23 2026, commit 1581d4cb.
  [SH]  Ryan Shea, "Sharper one-sample matroid prophet inequalities" /
        "Three-state generator encoding and restricted overlap", Oct 11 2026,
        commit 8cd13959.

Usage:
    python3 check_C.py             # full certificate at the shipped parameters
    python3 check_C.py --selftest  # reproduce the incumbent's published values
    python3 check_C.py --fraction  # emit numerator/denominator for exact_fraction.txt

Exit status: 0 = every exact condition holds, 1 = at least one failed (each
failing condition is named on stderr).
"""
import sys
from decimal import Decimal, localcontext
from fractions import Fraction as Q

# ---------------------------------------------------------------------------
# PARAMETERS  (the only place any value is written)
# ---------------------------------------------------------------------------
# Every value is exact: ints, or (numerator, denominator) pairs.  An increment-3
# style re-search touches this block and nothing else.
PARAMS = dict(
    kappa=164,                  # integer group-size threshold (as published)
    rho=(93, 256),              # rate of the D mask
    h=(3, 4),                   # rate of the H mask
    t=(23, 2 ** 18),            # rate of the C/T masks and of the max branch
    theta=(261, 256),           # rounding base step;  B = theta**L
    L=256,                      # number of rounding phases
    mu=(105, 8),                # generator-tilt exponent
    nu=(113, 8),                # witness-tilt exponent
    u=(1, 867),                 # generator tilt (paper: a)
    w=(1, 4088),                # witness tilt   (paper: b)
    v=(1, 624),                 # arrangement tilt
    d=(2024848371, 2000000000), # decay rate; source requires 0 < d < lambda
)

# The incumbent's parameter set (bound-111 as published), used only by
# --selftest to reproduce the published constants digit for digit.
RANK1_PARAMS = dict(PARAMS, kappa=164, u=(1, 864), w=(1, 4000), d=(253, 250))

# Published constants this checker must reproduce (never re-derived by hand).
R1_P = Q(24383141, 67108864)                                        # [R1 App.A]
R1_GAMMA = Q(69959099203, 812800834560)                             # [R1 App.A]
R1_EPSILON = Q(69328715, 2294341632)                                # [R1 App.A]
R1_S141 = Q(3932831273804099, 747774506088529920)                   # [R1 App.A]
R1_C141 = Q(165971304277649481670619, 324956758716416046811841770291200)   # [R1 (1)]
R1_CSTAR = Q(4084754449786906742230661, 8009094702029267287249256448000000)  # [R1 Intro]
OPENAI_293 = Q(1, 2 ** 293)                                         # [R1 App.B]


# ---------------------------------------------------------------------------
# Exact logarithm bounds (rational intervals; used only for the independent
# log-interval route to the two tilts and to lambda > d)
# ---------------------------------------------------------------------------
def _atanh_bounds(y, terms=24):
    """Interval for ln((1+y)/(1-y)) = 2*sum y^(2j+1)/(2j+1), 0 <= y <= 1/3."""
    assert 0 <= y <= Q(1, 3)
    total = sum((2 * y ** (2 * j + 1) / Q(2 * j + 1) for j in range(terms)), Q(0))
    tail = 2 * y ** (2 * terms + 1) / (Q(2 * terms + 1) * (1 - y * y))
    return total, total + tail


_LN2 = _atanh_bounds(Q(1, 3))


def ln_bounds(x, terms=24):
    """Rigorous (lower, upper) rational bounds on ln x for exact rational x > 0."""
    assert x > 0
    if x < 1:
        lo, hi = ln_bounds(1 / x, terms)
        return -hi, -lo
    k = x.numerator.bit_length() - x.denominator.bit_length()
    if Q(2) ** k > x:
        k -= 1
    y = x / Q(2) ** k                      # 1 <= y < 2   =>   (y-1)/(y+1) <= 1/3
    lo, hi = _atanh_bounds((y - 1) / (y + 1), terms)
    return lo + k * _LN2[0], hi + k * _LN2[1]


def _q(v):
    return Q(v) if isinstance(v, int) else Q(*v)


def build(params):
    """Derive every quantity the proof names, exactly, from the config block."""
    pr = {k: _q(v) for k, v in params.items()}
    kappa, rho, h, t = pr["kappa"], pr["rho"], pr["h"], pr["t"]
    theta, L, mu, nu = pr["theta"], pr["L"], pr["mu"], pr["nu"]
    u, w, v, d = pr["u"], pr["w"], pr["v"], pr["d"]

    K = kappa + nu                                     # [R1 §1]
    B = theta ** L                                     # [R1 §1] B = theta^L
    p = rho + (1 - rho) * t                            # [R1 §1]
    A = rho * (3 + 4 * v / 3)                          # [R1 App.A]
    bY = (Q(2, 3) * u * (1 / rho - 1) + w) / (1 + u) + 2 * v   # [R1 §1]
    gamma = rho / 4 - bY / d                           # [R1 §1]
    a0 = 1 / d                                         # [R1 §1]
    epsilon = mu * rho / kappa + u / d                 # [R1 §1]
    zeta = (1 - p) / (1 + p)                           # [R1 App.A]

    def L_of(x):        # loss L(x)                     [R1 App.A]
        return epsilon + K * t + (K * t + K * rho / kappa) / (x - 1)

    def s_of(x):        # slack s(x)                    [R1 App.A]
        return (1 - h) * (gamma - L_of(x) / h)

    def C_of(x):        # coefficient C(x)              [R1 App.A; eq.(5)]
        return (1 - t) * ((x - 1) / x) ** 2 * t * s_of(x) / (L * (theta - 1) * K)

    return dict(pr=pr, K=K, B=B, p=p, A=A, bY=bY, gamma=gamma, a0=a0,
                epsilon=epsilon, zeta=zeta, L_of=L_of, s_of=s_of, C_of=C_of)


# ---------------------------------------------------------------------------
# Reporting helpers
# ---------------------------------------------------------------------------
def sig(x, n=20):
    """Decimal rendering of a Fraction, rounded to n significant digits."""
    with localcontext() as ctx:
        ctx.prec = n
        return f"{Decimal(x.numerator) / Decimal(x.denominator):.{n - 1}e}"


def plain(x, n=17):
    """Decimal rendering of a Fraction without an exponent."""
    with localcontext() as ctx:
        ctx.prec = n
        return f"{Decimal(x.numerator) / Decimal(x.denominator):f}"


def fair_bits(r):
    """Number of fair coin flips needed for a dyadic rational in (0,1)."""
    den = r.denominator
    assert den & (den - 1) == 0, "%s has a non-dyadic denominator" % r
    return den.bit_length() - 1


# ---------------------------------------------------------------------------
# The certificate
# ---------------------------------------------------------------------------
def full_certificate(params, label):
    P = build(params)
    pr, kappa, rho, h, t = P["pr"], P["pr"]["kappa"], P["pr"]["rho"], P["pr"]["h"], P["pr"]["t"]
    theta, L, mu, nu = P["pr"]["theta"], P["pr"]["L"], P["pr"]["mu"], P["pr"]["nu"]
    u, w, v, d = P["pr"]["u"], P["pr"]["w"], P["pr"]["v"], P["pr"]["d"]
    p, B, A, gamma, a0, K = P["p"], P["B"], P["A"], P["gamma"], P["a0"], P["K"]

    lam_lo, lam_hi = ln_bounds(1 / p)                              # lambda = -ln p
    series_4 = sum((2 * P["zeta"] ** (2 * j + 1) / Q(2 * j + 1) for j in range(4)), Q(0))
    series_20 = sum((2 * P["zeta"] ** (2 * j + 1) / Q(2 * j + 1) for j in range(20)), Q(0))

    C_B, s_B = P["C_of"](B), P["s_of"](B)
    C_141, s_141 = P["C_of"](Q(141)), P["s_of"](Q(141))

    checks = []

    def cond(name, ok, cite):
        checks.append((name, bool(ok), cite))

    # --- the rate p -------------------------------------------------------
    cond("p = rho + (1-rho)t equals the published 24383141/67108864",
         p == R1_P, "[R1 App.A]")
    cond("p > (3/4)^4   (hence p^(-1/4) < 4/3)",
         p > Q(3, 4) ** 4, "[R1 App.A]")

    # --- base B ------------------------------------------------------------
    cond("B = theta^L exactly (rational, not a decimal interpolation)",
         B == theta ** L, "[R1 §1] B = theta^L")
    cond("B > 141   (261^256 > 141*256^256)",
         B > 141, "[R1 App.A]")
    cond("B > 140   (the incumbent's conservative evaluation)",
         B > 140, "[R1 Intro]")
    cond("L*(theta-1) = 5   (exact integer phase denominator)",
         L * (theta - 1) == 5, "[R1 App.A]")

    # --- the two tilts, primary route: exact integer powers ---------------
    cond("tilt 1 (integer powers): A^8 p^105 < (u v)^8",
         A ** 8 * p ** 105 < (u * v) ** 8, "[R1 App.A eq.(31)]")
    cond("tilt 2 (integer powers): (1-p)^8 p^113 < (w v)^8",
         (1 - p) ** 8 * p ** 113 < (w * v) ** 8, "[R1 App.A eq.(31)]")
    # --- the two tilts, second independent route: rigorous log intervals ---
    cond("tilt 1 (log interval): mu*lam_lo > ln_hi(A/(u v))",
         mu * lam_lo > ln_bounds(A / (u * v))[1], "[R1 §1 eq.(3); App.A]")
    cond("tilt 2 (log interval): nu*lam_lo > ln_hi((1-p)/(w v))",
         nu * lam_lo > ln_bounds((1 - p) / (w * v))[1], "[R1 §1 eq.(3); App.A]")

    # --- decay: 0 < d < lambda --------------------------------------------
    cond("0 < d", d > 0, "[R1 §1 eq.(4)]")
    cond("d < lambda, via the rigorous log interval (lam_lo > d)",
         lam_lo > d, "[R1 §1 eq.(4); App.A]")
    cond("d < lambda, via the positive zeta-series (20 terms > d)",
         series_20 > d,
         "[R1 App.A] (App.A truncates at 4 terms; every extra term is positive)")
    cond("d > 4*bY/rho   (so that gamma > 0)",
         4 * P["bY"] / rho < d, "[R1 §1] gamma = rho/4 - bY/d")

    # --- the structural scalar conditions ---------------------------------
    cond("0 < gamma   (gamma = rho/4 - bY/d)",
         gamma > 0, "[R1 §1 eq.(4)]")
    cond("gamma <= rho/4",
         gamma <= rho / 4, "[R1 §1 eq.(4)]")
    cond("s(B) > 0",
         s_B > 0, "[R1 §1 eq.(4)]")
    cond("(1-t)(gamma*kappa + a0)/K <= 1/4   (max-branch cancellation)",
         (1 - t) * (gamma * kappa + a0) / K <= Q(1, 4), "[R1 §1 eq.(4); §8 eq.(30)]")

    # --- parameter domains -------------------------------------------------
    cond("kappa >= 4 and integral",
         kappa >= 4 and kappa.denominator == 1, "[R1 §1; §8 threshold]")
    cond("0 < rho,h,t,u,w,v < 1",
         all(0 < z < 1 for z in (rho, h, t, u, w, v)), "[R1 §1]")
    cond("mu > 1/4, nu > 0, 8*mu and 8*nu integral",
         mu > Q(1, 4) and nu > 0 and 8 * mu == int(8 * mu) and 8 * nu == int(8 * nu),
         "[R1 §1; App.A eq.(31) uses 8*mu=105, 8*nu=113]")
    cond("d > 0 and u,w,v > 0  (all tilts positive before taking roots)",
         d > 0 and u > 0 and w > 0 and v > 0, "[R1 App.A eq.(31)]")
    cond("seed accounting 47n+27: h, rho, t dyadic, 47 per label + 27 shared",
         (fair_bits(rho) + fair_bits(h) + 2 * fair_bits(t) + 1,
          8 + fair_bits(1 - t) + 1) == (47, 27),
         "[R1 Theorem 1; §1]")

    # --- monotonicity in x and the strict improvement ---------------------
    cond("C(x) increasing: s(B) > s(141) and ((B-1)/B)^2 > (140/141)^2",
         s_B > s_141 and ((B - 1) / B) ** 2 > Q(140, 141) ** 2, "[R1 App.A]")
    cond("C(B) > C(141) at the shipped parameters",
         C_B > C_141, "[R1 App.A]")
    cond("C(B) > C141 (incumbent board rank 1)",
         C_B > R1_C141, "[R1 eq.(5); App.B]")
    cond("C(B) > C* (Shea's published certificate)",
         C_B > R1_CSTAR, "[R1 Intro; App.B]")
    cond("C(B) > 2^-293 (OpenAI's internal fixed-vector accounting)",
         C_B > OPENAI_293, "[R1 App.B]")

    failures = [c for c in checks if not c[1]]
    print("=" * 78)
    print("%s: %d exact rational conditions" % (label, len(checks)))
    print("=" * 78)
    for i, (name, ok, cite) in enumerate(checks, 1):
        print("[%02d] %s  %-68s %s" % (i, "PASS" if ok else "FAIL", name, cite))
    print("-" * 78)
    print("p        = %s" % p)
    print("lambda   = %s  <=  -ln p  <=  %s   (rigorous rational interval)"
          % (sig(lam_lo, 20), sig(lam_hi, 20)))
    print("B        = (theta)^L = (%s)^%d" % (theta, L))
    print("B        = %.17f   > 141" % float(B))
    print("gamma    = %s" % gamma)
    print("s(141)   = %s" % s_141)
    print("s(B)     = positive (asserted exactly above)" if s_B > 0 else "s(B) <= 0")
    print("-" * 78)
    print("exact C (numerator, then denominator; both exact integers):")
    print("  %d" % C_B.numerator)
    print("  %d" % C_B.denominator)
    print("decimal C = %s   (20 significant digits)" % sig(C_B))
    print("decimal C141 (incumbent) = %s" % sig(R1_C141))
    print("ratio C / C141 = %s   (+%s%% over the incumbent)"
          % (plain(C_B / R1_C141, 17), plain((C_B / R1_C141 - 1) * 100, 6)))
    print("=" * 78)
    if failures:
        for name, _, cite in failures:
            print("FAILED: %s   %s" % (name, cite), file=sys.stderr)
        print("RESULT: FAIL (%d/%d)" % (len(failures), len(checks)), file=sys.stderr)
        return 1, C_B
    print("RESULT: PASS (%d/%d exact rational conditions)" % (len(checks), len(checks)))
    return 0, C_B


def selftest():
    """Reproduce the incumbent's published values digit for digit.

    This is what certifies the checker itself: the same code path that produces
    the shipped coefficient must reproduce p, gamma, epsilon, s(141), C(141) and
    C*, all as exact rationals, at the bound-111 parameter set.
    """
    P = build(RANK1_PARAMS)
    c141, s141 = P["C_of"](Q(141)), P["s_of"](Q(141))
    c140 = P["C_of"](Q(140))
    cB = P["C_of"](P["B"])
    cases = [
        ("p = 24383141/67108864", P["p"], R1_P, "[R1 App.A]"),
        ("gamma = 69959099203/812800834560", P["gamma"], R1_GAMMA, "[R1 App.A]"),
        ("epsilon = 69328715/2294341632", P["epsilon"], R1_EPSILON, "[R1 App.A]"),
        ("s(141) = 3932831273804099/747774506088529920", s141, R1_S141, "[R1 App.A]"),
        ("C(140) = C* (Shea)", c140, R1_CSTAR, "[R1 Intro]"),
        ("C(141) = C141 (board rank 1)", c141, R1_C141, "[R1 eq.(1)]"),
    ]
    print("=" * 78)
    print("SELFTEST: reproduce the incumbent's published constants exactly")
    print("=" * 78)
    ok = True
    for name, got, want, cite in cases:
        same = got == want
        ok = ok and same
        print("[%s] %-48s %s" % ("PASS" if same else "FAIL", name, cite))
    # the incumbent's own published decimals, reproduced from the exact value
    dec_ok = sig(c141, 16) == "5.107488914317048e-10"
    ok = ok and dec_ok
    print("[%s] C(141) = %s  (board rank-1 row displays 5.107488914317048e-10)"
          % ("PASS" if dec_ok else "FAIL", sig(c141, 16)))
    c1_ok = sig(cB, 16) == "5.110608508730857e-10"
    ok = ok and c1_ok
    print("[%s] C(B)   = %s  (Increment 1 published 5.110608508730857e-10)"
          % ("PASS" if c1_ok else "FAIL", sig(cB, 16)))
    print("=" * 78)
    print("RESULT: %s" % ("PASS (checker reproduces the incumbent digit for digit)"
                          if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--selftest" in args:
        sys.exit(selftest())
    code, C = full_certificate(PARAMS, "SHIPPED PARAMETERS (Increments 1+2+3)")
    if "--fraction" in args:
        print("\n%d\n%d" % (C.numerator, C.denominator))
    sys.exit(code)
