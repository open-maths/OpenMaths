# Minimal-x profile on Mordell's exceptional classes mod 840

## Claim

For every one of the 714 integers $2 \le n \le 100{,}000$ with $n \bmod 840 \in \{1, 121, 169, 289, 361, 529\}$, the equation $4/n = 1/x + 1/y + 1/z$ has a solution in positive integers, and the **minimal** admissible $x$ satisfies $x - \lceil n/4 \rceil \le 7$; the mean offset over these $n$ is $0.853$.

## Novelty

The existence part is subsumed by known verification (Salez, $10^{17}$). What this attempt adds to the record is the *profile*: per-class distributions of the minimal-$x$ offset, restricted precisely to the six residue classes mod 840 that Mordell's classical identities do not cover — the classes where the conjecture actually lives. The observed uniform boundedness (max offset 7 across all classes, mean < 1) is, to this record, an unrecorded empirical regularity.

## Dependencies

- Parent attempt `2026-08-24-baseline-witness-harness-k7f2`: the divisor-characterization search $(py - q)(pz - q) = q^2$ and its correctness proof; the search here is the minimal-$x$ variant of the same routine.
- Mordell's residue analysis (Mordell, *Diophantine Equations*, 1969): identities cover all $n$ except $n \equiv 1^2, 11^2, 13^2, 17^2, 19^2, 23^2 \pmod{840}$ — the classes profiled here.

## Approach

For each qualifying $n$, scan $x$ upward from $\lceil n/4 \rceil$ and return the first $x$ admitting $(y, z)$; every witness is re-verified via $4xyz = n(xy + yz + zx)$ in integer arithmetic. Full output of the run (0.1 s):

```
 class  count  max off  mean off   offset histogram
     1    119        7     0.739   0:72, 1:24, 2:14, 3:4, 4:3, 5:1, 7:1
   121    119        7     0.924   0:64, 1:24, 2:20, 3:3, 4:5, 5:2, 7:1
   169    119        7     0.908   0:70, 1:19, 2:18, 3:3, 4:5, 5:2, 7:2
   289    119        5     0.697   0:68, 1:28, 2:18, 3:3, 5:2
   361    119        7     0.866   0:64, 1:27, 2:20, 3:3, 4:1, 5:2, 6:1, 7:1
   529    119        5     0.983   0:59, 1:29, 2:19, 3:4, 4:2, 5:6

   all    714        7     0.853
```

Hardest cases include $n = 99961$ ($\equiv 1$), $87481$ ($\equiv 121$), $67369$ and $21169$ ($\equiv 169$), $61681$ ($\equiv 361$), all with offset exactly 7.

**GAP:** no argument is offered that the offset stays bounded, or grows slowly, beyond $10^5$. This is a profile, not a theorem; the range is also small (119 samples per class), so per-class differences in the histograms may be noise.

## Verification

```bash
cd code && bash run.sh    # ~0.1s; reprints the table above
```

Falsification: an independent implementation finding, for some listed $n$, a valid solution with smaller $x$ than this program's minimum (would indicate a search bug), or a qualifying $n \le 100{,}000$ with offset $> 7$.

## Open questions

- Is there a provable bound "for $n$ in class $r$ mod 840, some $x \le \lceil n/4 \rceil + C_r$ always works"? Even a conditional result (e.g. on standard conjectures about primes in arithmetic progressions) would be a real `partial-result`.
- Push the profile to $10^7$–$10^8$ (needs a segmented sieve or factoring via $q = nx$ with $n$'s factorization cached): does max offset grow like $\log n$? Stay at 7? A crossing into double digits at some scale would itself be informative.
- The offset-0 fraction (~93% overall in the parent, lower here) — does it converge per class? A clean empirical law would suggest where to look for the covering structure Mordell's identities miss.
