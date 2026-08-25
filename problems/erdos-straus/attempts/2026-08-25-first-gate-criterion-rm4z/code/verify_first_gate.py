#!/usr/bin/env python3
"""Exact checks for the first-gate factor criterion.

No floating point and no third-party dependency is used.  The symbolic check
expands polynomials as dictionaries from monomials to integer coefficients.
The finite run corroborates (but is not the proof of) the unbounded theorem.
"""

import argparse
import math
from collections import Counter


MORDELL_CLASSES = (1, 121, 169, 289, 361, 529)
PROFILE_OFFSET_ZERO = {1: 72, 121: 64, 169: 70, 289: 68, 361: 64, 529: 59}
N_VARS = 5  # x, n, q, d, e


def poly_const(value):
    return {} if value == 0 else {(0,) * N_VARS: value}


def poly_var(index):
    powers = [0] * N_VARS
    powers[index] = 1
    return {tuple(powers): 1}


def poly_add(left, right):
    out = dict(left)
    for monomial, coefficient in right.items():
        out[monomial] = out.get(monomial, 0) + coefficient
        if out[monomial] == 0:
            del out[monomial]
    return out


def poly_scale(coefficient, value):
    return {m: coefficient * c for m, c in value.items() if coefficient * c}


def poly_sub(left, right):
    return poly_add(left, poly_scale(-1, right))


def poly_mul(left, right):
    out = {}
    for lm, lc in left.items():
        for rm, rc in right.items():
            monomial = tuple(a + b for a, b in zip(lm, rm))
            out[monomial] = out.get(monomial, 0) + lc * rc
    return {m: c for m, c in out.items() if c}


def symbolic_identity_check():
    """Check an exact polynomial certificate for the witness identity.

    Put 3y=q+d and 3z=q+e.  If 4x-n=3, nx=q, and de=q^2,
    the cross-multiplied Erdős--Straus difference is zero.  We verify the
    stronger polynomial identity expressing nine times that difference as an
    integer combination of those three defining relations.
    """
    x, n, q, d, e = (poly_var(i) for i in range(N_VARS))
    three = poly_const(3)
    y3 = poly_add(q, d)
    z3 = poly_add(q, e)
    product = poly_mul(y3, z3)
    residual_sum = poly_add(poly_add(poly_scale(2, q), d), e)

    # 9 * (4xyz - n(xy + yz + zx)), after 3y=q+d and 3z=q+e.
    lhs = poly_sub(
        poly_scale(4, poly_mul(x, product)),
        poly_mul(
            n,
            poly_add(
                poly_add(poly_scale(3, poly_mul(x, y3)), product),
                poly_scale(3, poly_mul(x, z3)),
            ),
        ),
    )

    relation_4x = poly_sub(poly_sub(poly_scale(4, x), n), three)
    relation_q = poly_sub(poly_mul(n, x), q)
    relation_de = poly_sub(poly_mul(d, e), poly_mul(q, q))
    rhs = poly_add(
        poly_add(
            poly_mul(relation_4x, product),
            poly_scale(-3, poly_mul(relation_q, residual_sum)),
        ),
        poly_scale(3, relation_de),
    )
    assert lhs == rhs


def build_spf(limit):
    spf = list(range(limit + 1))
    for p in range(2, math.isqrt(limit) + 1):
        if spf[p] != p:
            continue
        for multiple in range(p * p, limit + 1, p):
            if spf[multiple] == multiple:
                spf[multiple] = p
    return spf


def factorize(value, spf):
    factors = Counter()
    while value > 1:
        prime = spf[value]
        factors[prime] += 1
        value //= prime
    return factors


def merged_factorization(left, right):
    result = Counter(left)
    result.update(right)
    return result


def divisor_residues_of_square(factors, modulus):
    """Residues of every divisor of q^2, constructed from q's factorization."""
    residues = {1 % modulus}
    for prime, exponent in factors.items():
        powers = [pow(prime, k, modulus) for k in range(2 * exponent + 1)]
        residues = {(old * power) % modulus for old in residues for power in powers}
    return residues


def is_witness(n, x, y, z):
    return (
        0 < x <= y <= z
        and 4 * x * y * z == n * (x * y + y * z + z * x)
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=100_000)
    args = parser.parse_args()
    if args.limit < 13:
        raise SystemExit("limit must be at least 13")

    symbolic_identity_check()
    spf = build_spf(args.limit)
    checked = 0
    successes = 0
    class_totals = Counter()
    class_successes = Counter()

    for n in range(13, args.limit + 1, 12):
        x = (n + 3) // 4
        q = n * x
        factors = merged_factorization(factorize(n, spf), factorize(x, spf))
        assert q % 3 == 1

        qualifying_primes = sorted(p for p in factors if p % 3 == 2)
        criterion = bool(qualifying_primes)
        direct_divisor_gate = (-q) % 3 in divisor_residues_of_square(factors, 3)
        assert criterion == direct_divisor_gate

        checked += 1
        residue = n % 840
        if residue in MORDELL_CLASSES:
            class_totals[residue] += 1

        if criterion:
            ell = qualifying_primes[0]
            assert q % ell == 0
            y = (q + ell) // 3
            z = (q + q * q // ell) // 3
            assert (q + ell) % 3 == 0
            assert (q + q * q // ell) % 3 == 0
            assert is_witness(n, x, y, z)
            successes += 1
            if residue in MORDELL_CLASSES:
                class_successes[residue] += 1

    mordell_total = sum(class_totals.values())
    mordell_success = sum(class_successes.values())
    if args.limit == 100_000:
        assert class_totals == Counter({residue: 119 for residue in MORDELL_CLASSES})
        assert class_successes == Counter(PROFILE_OFFSET_ZERO)

    print("SYMBOLIC VERIFIED: the explicit witness identity reduces exactly")
    print(
        f"FINITE CHECK: criterion agrees with the direct divisor gate for all "
        f"{checked} integers n <= {args.limit} with n mod 12 = 1"
    )
    print(f"FIRST-GATE SUCCESSES: {successes} of {checked}")
    print(
        f"MORDELL CLASSES: {mordell_success} of {mordell_total}; "
        + ", ".join(f"{r}:{class_successes[r]}" for r in MORDELL_CLASSES)
    )


if __name__ == "__main__":
    main()
