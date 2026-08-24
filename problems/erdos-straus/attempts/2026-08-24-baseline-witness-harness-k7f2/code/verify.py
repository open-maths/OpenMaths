#!/usr/bin/env python3
"""Exhaustive Erdos-Straus verification over 2 <= n <= LIMIT, exact arithmetic only.

For each n a witness (x, y, z) with 4/n = 1/x + 1/y + 1/z is found and checked
via the cross-multiplied integer identity 4xyz == n(xy + yz + zx).

Method:
  n even          -> identity (m, m+1, m(m+1)),           m = n/2      [4/n = 2/m]
  n ≡ 3 (mod 4)   -> identity (a+1, a(a+1), n*a),         a = (n+1)/4
  n ≡ 1 (mod 4), 3|n -> identity (m, 3m+1, 3m(3m+1)),     m = n/3
  otherwise       -> divisor search: for x in (n/4, 3n/4], with p = 4x-n, q = nx,
                     solutions of 1/y + 1/z = p/q correspond to divisors d | q^2,
                     d <= q, via (py - q)(pz - q) = q^2; take y = (q+d)/p,
                     z = (q + q^2/d)/p when both are integers.

Every witness from every branch is re-checked by the integer identity before
being counted. No floating point anywhere.
"""

import argparse
import sys
from collections import Counter


def build_spf(limit: int) -> list:
    """Smallest-prime-factor sieve."""
    spf = list(range(limit + 1))
    i = 2
    while i * i <= limit:
        if spf[i] == i:
            for j in range(i * i, limit + 1, i):
                if spf[j] == j:
                    spf[j] = i
        i += 1
    return spf


def factorize(m: int, spf: list) -> dict:
    fac = {}
    while m > 1:
        p = spf[m]
        e = 0
        while m % p == 0:
            m //= p
            e += 1
        fac[p] = fac.get(p, 0) + e
    return fac


def divisors_of_square(fac: dict) -> list:
    """All divisors of (prod p^e)^2 given the factorization of the base."""
    divs = [1]
    for p, e in fac.items():
        divs = [d * p**k for d in divs for k in range(2 * e + 1)]
    return divs


def is_witness(n: int, x: int, y: int, z: int) -> bool:
    return (
        x > 0 and y > 0 and z > 0
        and 4 * x * y * z == n * (x * y + y * z + z * x)
    )


def search(n: int, spf: list):
    """Divisor-characterization search. Returns (x, y, z, x_offset) or None."""
    fac_n = factorize(n, spf)
    x_lo = n // 4 + 1
    for x in range(x_lo, (3 * n) // 4 + 1):
        p = 4 * x - n
        q = n * x
        fac_q = dict(fac_n)
        for pr, e in factorize(x, spf).items():
            fac_q[pr] = fac_q.get(pr, 0) + e
        q2 = q * q
        for d in divisors_of_square(fac_q):
            if d > q:
                continue
            if (q + d) % p != 0:
                continue
            zz_num = q + q2 // d
            if zz_num % p != 0:
                continue
            y = (q + d) // p
            z = zz_num // p
            if is_witness(n, x, y, z):
                return x, y, z, x - x_lo
    return None


def solve(n: int, spf: list):
    """Returns (method, x, y, z, x_offset_or_None)."""
    if n % 2 == 0:
        m = n // 2
        return "even", m, m + 1, m * (m + 1), None
    if n % 4 == 3:
        a = (n + 1) // 4
        return "3mod4", a + 1, a * (a + 1), n * a, None
    if n % 3 == 0:
        m = n // 3
        return "mult3", m, 3 * m + 1, 3 * m * (3 * m + 1), None
    res = search(n, spf)
    if res is None:
        return "NONE", 0, 0, 0, None
    x, y, z, off = res
    return "search", x, y, z, off


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--limit", type=int, default=100000)
    ap.add_argument("--witness", type=int, help="print the witness for a single n and exit")
    args = ap.parse_args()

    spf = build_spf(max(args.limit, args.witness or 2, 100))

    if args.witness:
        n = args.witness
        method, x, y, z, off = solve(n, spf)
        ok = is_witness(n, x, y, z)
        print(f"n={n}: 4/{n} = 1/{x} + 1/{y} + 1/{z}  [method={method}, verified={ok}]")
        return 0 if ok else 1

    methods = Counter()
    offsets = Counter()
    hardest = []  # (offset, n, x, y, z), kept small

    for n in range(2, args.limit + 1):
        method, x, y, z, off = solve(n, spf)
        if method == "NONE" or not is_witness(n, x, y, z):
            print(f"COUNTEREXAMPLE CANDIDATE OR BUG: n={n}", file=sys.stderr)
            return 2
        methods[method] += 1
        if off is not None:
            offsets[off] += 1
            hardest.append((off, n, x, y, z))
            hardest.sort(reverse=True)
            del hardest[5:]

    total = sum(methods.values())
    print(f"VERIFIED: 4/n = 1/x + 1/y + 1/z has a positive-integer solution for all 2 <= n <= {args.limit}")
    print(f"\nwitnesses by method (out of {total}):")
    for method, count in methods.most_common():
        print(f"  {method:>7}: {count}")
    if offsets:
        searched = sum(offsets.values())
        max_off = max(offsets)
        mean_off = sum(o * c for o, c in offsets.items()) / searched
        print(f"\ndivisor-search cases: {searched}")
        print(f"  x offset beyond ceil(n/4): max={max_off}, mean={mean_off:.3f}")
        print(f"  offset distribution (offset: count): "
              + ", ".join(f"{o}: {offsets[o]}" for o in sorted(offsets)[:10])
              + (" ..." if len(offsets) > 10 else ""))
        print("  hardest cases (largest minimal-x offset among searched):")
        for off, n, x, y, z in hardest:
            print(f"    n={n} (n mod 840 = {n % 840}): offset={off}, witness 4/{n} = 1/{x} + 1/{y} + 1/{z}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
