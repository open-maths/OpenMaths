#!/usr/bin/env python3
"""Minimal-x profile of the Erdos-Straus equation on Mordell's exceptional
residue classes mod 840, for n <= LIMIT. Exact arithmetic only.

For each n <= LIMIT with n mod 840 in {1, 121, 169, 289, 361, 529} (all such n
are odd and coprime to 840's relevant small primes in the hard direction),
find the minimal x > n/4 admitting positive integers y <= z with
4/n = 1/x + 1/y + 1/z, via the divisor characterization
(py - q)(pz - q) = q^2, p = 4x - n, q = nx. Record the offset
x_min - ceil(n/4) per class.

These classes are exactly the ones not covered by Mordell's classical
identities, hence the interesting ones to profile.
"""

import argparse
import sys
from collections import Counter, defaultdict

MORDELL_CLASSES = (1, 121, 169, 289, 361, 529)


def build_spf(limit: int) -> list:
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
    divs = [1]
    for p, e in fac.items():
        divs = [d * p**k for d in divs for k in range(2 * e + 1)]
    return divs


def is_witness(n: int, x: int, y: int, z: int) -> bool:
    return x > 0 and y > 0 and z > 0 and 4 * x * y * z == n * (x * y + y * z + z * x)


def minimal_x(n: int, spf: list):
    """Smallest x > n/4 admitting a solution; returns (x, y, z, offset)."""
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
            if d > q or (q + d) % p:
                continue
            zz = q + q2 // d
            if zz % p:
                continue
            y, z = (q + d) // p, zz // p
            if is_witness(n, x, y, z):
                return x, y, z, x - x_lo
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--limit", type=int, default=100000)
    args = ap.parse_args()

    spf = build_spf(args.limit)
    per_class = defaultdict(Counter)  # class -> Counter(offset)
    hardest = []

    count = 0
    for n in range(2, args.limit + 1):
        r = n % 840
        if r not in MORDELL_CLASSES:
            continue
        count += 1
        res = minimal_x(n, spf)
        if res is None:
            print(f"COUNTEREXAMPLE CANDIDATE OR BUG: n={n}", file=sys.stderr)
            return 2
        x, y, z, off = res
        per_class[r][off] += 1
        hardest.append((off, n, x, y, z))
        hardest.sort(reverse=True)
        del hardest[10:]

    print(f"PROFILED: minimal-x offsets for all {count} values n <= {args.limit} "
          f"with n mod 840 in {MORDELL_CLASSES}; a solution exists for every one.")
    print(f"\n{'class':>6} {'count':>6} {'max off':>8} {'mean off':>9}   offset histogram")
    all_offsets = Counter()
    for r in MORDELL_CLASSES:
        c = per_class[r]
        all_offsets.update(c)
        total = sum(c.values())
        mean = sum(o * k for o, k in c.items()) / total if total else 0.0
        hist = ", ".join(f"{o}:{c[o]}" for o in sorted(c))
        print(f"{r:>6} {total:>6} {max(c) if c else 0:>8} {mean:>9.3f}   {hist}")
    total = sum(all_offsets.values())
    mean = sum(o * k for o, k in all_offsets.items()) / total
    print(f"\n   all {total:>6} {max(all_offsets):>8} {mean:>9.3f}")
    print("\nhardest cases (largest minimal-x offset):")
    for off, n, x, y, z in hardest:
        print(f"  n={n} (mod 840 = {n % 840}): offset={off}, 4/{n} = 1/{x} + 1/{y} + 1/{z}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
