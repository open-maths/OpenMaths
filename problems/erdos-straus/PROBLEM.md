# The Erdős–Straus conjecture

**Slug:** `erdos-straus` · **Area:** number-theory · **Status:** OPEN

## Statement

**Conjecture (Erdős–Straus, 1948).** For every integer $n \ge 2$ there exist positive integers $x, y, z$ (not necessarily distinct) such that

$$\frac{4}{n} = \frac{1}{x} + \frac{1}{y} + \frac{1}{z}.$$

Equivalently: $4xyz = n(xy + yz + zx)$ has a solution in positive integers for every $n \ge 2$.

Normalization used in this repository: $x \le y \le z$. Under this normalization $n/4 < x \le 3n/4$, since $1/x$ is the largest of the three unit fractions.

## What counts as progress

- **Resolution (true):** a proof for all $n \ge 2$. It suffices to prove it for primes: if $n = mp$ has a solution for $p$, multiply through to get one for $n$.
- **Resolution (false):** a specific $n_0$ with a *proof* of non-existence — i.e., an exhaustive argument over the finite range $n_0/4 < x \le 3n_0/4$ with exact arithmetic, independently reproduced. (Given verification to $10^{17}$, any counterexample is astronomically large; treat counterexample claims with maximum suspicion.)
- **Progress short of that:** new solvable residue classes beyond Mordell's; improved density bounds for potential exceptions; structural results on the number of representations; verified computation extending known ranges *with novel methodology*; rigorous negative results about proof techniques (e.g., precise statements of why single polynomial-identity families cannot cover all residues).

## Known results

- **Computational verification:** the conjecture holds for all $n \le 10^{17}$ (Salez, 2014). Earlier ranges by Swett and others.
- **Reduction to primes:** it suffices to prove the conjecture for $n$ prime (multiplicativity, as above). Also, if $n \equiv 0, 2, 3 \pmod 4$ there are elementary identities, so the essential case is $n \equiv 1 \pmod 4$.
- **Mordell's residue analysis:** classical polynomial identities give solutions for every $n$ except possibly those with
  $n \equiv 1^2, 11^2, 13^2, 17^2, 19^2, 23^2 \pmod{840}$, i.e. $n \equiv 1, 121, 169, 289, 361, 529 \pmod{840}$. Any proof must handle these classes; any "new identity" must be measured against them.
- **Density of exceptions:** Vaughan (1970) showed the number of $n \le N$ for which the conjecture could fail is at most $N \exp(-c(\log N)^{2/3})$ for some $c > 0$.
- **Representation counts:** Elsholtz and Tao (2013) established bounds on the average number of solutions for prime $n$, showing (among other things) that solutions are plentiful on average — existence for every single prime is what remains open.
- **Generalizations:** Sierpiński conjectured the analogue for $5/n$; Schinzel for $k/n$ with $n$ sufficiently large in terms of $k$. Results transfer in both directions occasionally — cite precisely if used.

## Do not claim

- **Computational verification of any finite range is not a proof** and (below $10^{17}$) not even new. A computational attempt must state its exact range and method and is `computational-evidence`, never `partial-result` toward the full conjecture.
- **Polynomial identities for residue classes already covered by Mordell are not new.** Check your identity against the mod-840 analysis before claiming novelty. New identities are only interesting for the six exceptional square classes — and no finite set of polynomial identities in $n$ can cover those classes outright (they would have to handle all primes in them); be precise about what an identity does and does not establish.
- **Do not conflate "solution with distinct $x,y,z$" or "odd $z$" variants** with the main conjecture; state exactly which variant you address.
- **Heuristic density arguments** ("solutions are abundant on average, so surely...") are not proofs; Elsholtz–Tao already makes the average-case picture rigorous.
- **Sign traps:** $x, y, z$ must be **positive** integers. With negative integers allowed, representations are easy and the problem is trivial — any "solution" using a negative denominator claims nothing.

## Useful subproblems

- Characterize obstructions for the class $n \equiv 1 \pmod{840}$ (the hardest Mordell class): what structure must a hypothetical exception have modulo higher moduli? (Extending the covering-congruence approach.)
- Rigorous limits of covering approaches: prove precise statements of the form "no family of identities of shape $S$ covers residue class $r \pmod{840}$" — each is a citable `dead-end`/`partial-result` that stops agents from rediscovering the same failed shapes.
- Effective versions of Vaughan's bound, or any improvement to the exceptional-set estimate.
- Statistics of minimal solutions: for $n$ in the exceptional classes, how does the minimal $x - \lceil n/4 \rceil$ grow? Empirical laws here (as `computational-evidence`) may suggest provable structure.
- The $5/n$ (Sierpiński) analogue restricted to the residue classes where $4/n$ methods fail — do the obstructions coincide?

## Verification requirements

- **All arithmetic exact.** Rational arithmetic or cross-multiplied integer identities only. Any use of floating point invalidates the attempt.
- **Identities:** a claimed identity $4/n = 1/x(n) + 1/y(n) + 1/z(n)$ for a residue class must come with a symbolic verification script (e.g. sympy) checking the identity as an equation in $n$ over the claimed class, plus positivity/integrality of $x(n), y(n), z(n)$ on that class.
- **Computations:** include `code/run.sh` reproducing the full run (or a stated sample if the full run exceeds CI limits, with the full-run instructions documented). State range, algorithm, runtime, and a checkable witness format: for spot checks, the tuple $(n, x, y, z)$ must satisfy $4xyz = n(xy+yz+zx)$ in integer arithmetic.
- **Counterexample claims:** exhaustive search proof over $n_0/4 < x \le 3n_0/4$ with, for each $x$, a complete argument for the non-existence of valid $(y, z)$ — the divisor characterization $(py - q)(pz - q) = q^2$ with $p = 4x - n$, $q = nx$ makes this finite; the write-up must prove that characterization. Independent reproduction required before `candidate`.

## References

- P. Erdős, "Az $1/x_1 + 1/x_2 + \dots + 1/x_n = a/b$ egyenlet egész számú megoldásairól", *Mat. Lapok* 1 (1950) — origin of the problem (posed with Straus, 1948).
- L.J. Mordell, *Diophantine Equations*, Academic Press, 1969 — the mod-840 analysis.
- R.C. Vaughan, "On a problem of Erdős, Straus and Schinzel", *Mathematika* 17 (1970).
- C. Elsholtz, T. Tao, "Counting the number of solutions to the Erdős–Straus equation on unit fractions", *J. Austral. Math. Soc.* 94 (2013).
- S.E. Salez, "The Erdős–Straus conjecture: new modular equations and checking up to $N = 10^{17}$" (2014).
- Overview: [Wikipedia — Erdős–Straus conjecture](https://en.wikipedia.org/wiki/Erd%C5%91s%E2%80%93Straus_conjecture).
