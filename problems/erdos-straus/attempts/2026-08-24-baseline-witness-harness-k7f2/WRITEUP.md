# Baseline witness harness: Erdős–Straus verified for n ≤ 100,000

## Claim

For every integer $2 \le n \le 100{,}000$ there exist positive integers $x \le y \le z$ with $4/n = 1/x + 1/y + 1/z$. The included program constructs an explicit witness $(x, y, z)$ for each such $n$ and re-verifies every witness with the exact integer identity $4xyz = n(xy + yz + zx)$. No floating point is used anywhere.

## Novelty

**Nothing mathematically new.** The conjecture is known to hold to $10^{17}$ (Salez, 2014), so this range adds no evidence. The contribution is infrastructural: a small, dependency-free, exact-arithmetic harness that (a) seeds this problem's research graph with a reproducible baseline, and (b) gives later attempts a reusable solver — in particular the divisor-characterization search, which finds the **minimal** admissible $x$ and thereby exposes structure (see Open questions).

## Dependencies

- Classical identities (all verified by the harness on every use):
  - $n = 2m$: $\;4/n = 2/m = 1/m + 1/(m{+}1) + 1/(m(m{+}1))$.
  - $n \equiv 3 \pmod 4$, $a = (n{+}1)/4$: $\;4/n = 1/(a{+}1) + 1/(a(a{+}1)) + 1/(na)$.
  - $n = 3m$ odd: $\;4/n = 1/m + 1/(3m{+}1) + 1/(3m(3m{+}1))$.
- Divisor characterization: for $p = 4x - n > 0$, $q = nx$, solutions of $1/y + 1/z = p/q$ with $y \le z$ correspond exactly to divisors $d \mid q^2$, $d \le q$, with $p \mid (q + d)$ and $p \mid (q + q^2/d)$, via $(py - q)(pz - q) = q^2$. Proof: rearrange $qz + qy = pyz$ as $p^2yz - pqy - pqz = 0$, add $q^2$ to both sides and factor.
- No parent attempts.

## Approach

For each $n$: even, $\equiv 3 \pmod 4$, and odd-multiple-of-3 cases are dispatched to the identities above (covering $5/6$ of all $n$). The remaining cases ($n \equiv 1 \pmod 4$, $3 \nmid n$; 16,666 values in range) are solved by scanning $x$ from $\lceil n/4 \rceil$ upward and enumerating divisors of $q^2$ from the prime factorization of $q = nx$ (smallest-prime-factor sieve; no trial division at query time). Every branch's output is re-checked by the integer identity before being counted, so a bug in any identity or in the search would surface as a hard failure, not a silent wrong answer.

Results of the full run (1.2 s on a laptop):

```
witnesses by method (out of 99999):   even: 50000 · 3mod4: 25000 · search: 16666 · mult3: 8333
divisor-search cases: minimal-x offset beyond ceil(n/4): max = 7, mean = 0.086
offset distribution: 0: 15533, 1: 967, 2: 109, 3: 20, 4: 16, 5: 15, 6: 1, 7: 5
```

All five cases with the maximal offset 7 have $n \bmod 840 \in \{1, 121, 169, 361\}$ — Mordell's exceptional classes.

## Verification

```bash
cd code && bash run.sh            # full range, ~2s; prints VERIFIED + statistics
python3 verify.py --witness 1201  # spot-check any single n
```

Falsification: any $n \le 100{,}000$ for which the program's witness fails the integer identity, or any independent implementation finding some $n$ in range with no solution, refutes this claim. CI runs `run.sh` on every validation pass.

## Open questions

- The minimal-$x$ offset is 0 for 93% of searched $n$ and its largest values concentrate in Mordell's exceptional classes mod 840. Is there a provable statement behind that concentration? (Profiled further in `2026-08-24-mordell-class-profile-x2d7`.)
- Does the minimal offset grow (empirically) like any recognizable function of $n$ — and can an upper bound on it be proven for any residue class? A proven bound of the form "offset $\le f(n)$" for a class would make verification on that class a finite computation per $n$ with explicit constants.
