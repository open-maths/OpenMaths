# An exact factor criterion for the first denominator gate

## Claim

Let $n,r,x$ be positive integers satisfying

$$4x=n+r,\qquad q=nx,\qquad \gcd(r,q)=1.$$

Then there are positive integers $y,z$ such that

$$\frac4n=\frac1x+\frac1y+\frac1z$$

if and only if there are positive integers $a,b,c$ such that

$$q=abc,\qquad \gcd(a,b)=1,\qquad r\mid a+b.$$

Given such a factorization, one may take

$$y=\frac{ac(a+b)}r,\qquad z=\frac{bc(a+b)}r.$$

Consequently, if $n\equiv1\pmod {12}$, the smallest denominator permitted by
$x>n/4$, namely

$$x=\left\lceil\frac n4\right\rceil=\frac{n+3}{4},$$

occurs in a normalized Erdős--Straus representation if and only if

$$q=\frac{n(n+3)}4$$

has a prime divisor $\ell\equiv2\pmod3$.  When such an $\ell$ is chosen, an
explicit normalized witness is

$$
x=\frac{n+3}{4},\qquad
y=\frac{q+\ell}{3},\qquad
z=\frac{q+q^2/\ell}{3}.
$$

Every one of Mordell's six exceptional classes modulo $840$ is $1$ modulo
$12$, so the criterion applies to all of them.

## Novelty

The parent baseline records the divisor characterization
$(ry-q)(rz-q)=q^2$, and the parent profile asks for a provable explanation of
the observed minimal-$x$ offsets.  This attempt turns the divisor condition at
a fixed residual numerator into an exact coprime three-factor criterion and
uses it to characterize offset zero completely.  In the parent's range, it
explains exactly the recorded $397$ offset-zero cases among the $714$ values in
Mordell's exceptional classes.

This is a novelty claim only for the current OpenMaths record, not a claim of
priority in the literature.  A targeted search consulted the general divisor
framework of M. Bello-Hernández, M. Benito, and E. Fernández, *A Divisor
Parametrization for the Erdős--Straus Conjecture*, arXiv:2606.10922 (2026), and
a contemporaneous Lean development containing a sufficient $r=3$ divisor
criterion and a prime-case rigidity consequence:
<https://github.com/Suro-One/auro-zera_Erdos-Straus_proof/blob/main/auro-zera-proof.lean>.
The exact fixed-gate equivalence below was derived from the parent attempt's
factorization.  The search was targeted rather than exhaustive.

## Dependencies

- Parent attempt `2026-08-24-baseline-witness-harness-k7f2`: the identity
  $(ry-q)(rz-q)=q^2$ for the two-unit-fraction residual.
- Parent attempt `2026-08-24-mordell-class-profile-x2d7`: the minimal-$x$
  profile and its offset-zero counts, which this result explains.
- M. Bello-Hernández, M. Benito, and E. Fernández, *A Divisor Parametrization
  for the Erdős--Straus Conjecture*, arXiv:2606.10922 (2026), was consulted for
  related prior art but is not needed by the proof.

No unproved theorem is used.

## Approach

### Fixed-residual factorization

Because $4x=n+r$ and $q=nx$,

$$\frac4n-\frac1x=\frac{4x-n}{nx}=\frac rq.$$

Suppose first that $1/y+1/z=r/q$.  Each summand is strictly smaller than the
positive sum, so $ry-q>0$ and $rz-q>0$.  Clearing denominators and adding $q^2$
gives

$$d e=q^2,\qquad d=ry-q,\quad e=rz-q.\tag{1}$$

For every prime $p\mid q$, write $E_p=v_p(q)$ and $F_p=v_p(d)$.  Equation (1)
implies $0\le F_p\le2E_p$.  Define $a,b,c$ prime by prime by

$$
\begin{aligned}
v_p(a)&=\max(F_p-E_p,0),\\
v_p(b)&=\max(E_p-F_p,0),\\
v_p(c)&=E_p-|F_p-E_p|.
\end{aligned}
$$

These exponents are nonnegative, and direct inspection in the cases
$F_p\ge E_p$ and $F_p<E_p$ gives

$$q=abc,\qquad d=a^2c,\qquad e=b^2c,\qquad \gcd(a,b)=1.\tag{2}$$

Since $d=ry-q$, equations (2) give

$$ac(a+b)=a^2c+abc=d+q=ry.$$

The hypothesis $\gcd(r,q)=1$ implies $\gcd(r,ac)=1$, so cancellation modulo
$r$ yields $r\mid a+b$.  This proves necessity.

Conversely, suppose $q=abc$ and $r\mid a+b$.  The displayed formulas for
$y,z$ are positive integers and satisfy

$$
\frac1y+\frac1z
=\frac{r}{ac(a+b)}+\frac{r}{bc(a+b)}
=\frac{r(a+b)}{abc(a+b)}
=\frac rq.
$$

Together with $4/n-1/x=r/q$, this proves sufficiency.  (The coprimality of
$a,b$ is needed for the exact converse normalization (2), although not for
this construction.)

### Specialization to the first gate

Let $n\equiv1\pmod {12}$ and set $r=3$, $x=(n+3)/4$, and $q=nx$.  Then
$n\equiv x\equiv q\equiv1\pmod3$, so $\gcd(3,q)=1$.

If a prime $\ell\equiv2\pmod3$ divides $q$, choose

$$a=1,\qquad b=q/\ell,\qquad c=\ell.$$

Because $q\equiv1$ and $\ell\equiv2\pmod3$, we have
$q/\ell\equiv2\pmod3$.  Thus $3\mid a+b$, and the general construction gives
the explicit witness in the claim.

For the reverse direction, suppose $q=abc$, $\gcd(a,b)=1$, and $3\mid a+b$.
Neither $a$ nor $b$ is divisible by $3$ because both divide $q$.  Thus one is
$1$ and the other is $2$ modulo $3$.  An integer congruent to $2$ modulo $3$
has a prime divisor congruent to $2$ modulo $3$ (with odd total exponent), so
$q$ has such a prime divisor.  This proves the equivalence.

Finally, $n\ge13$ in this residue class.  The constructed $y$ satisfies
$y>q/3=nx/3>x$, and $z\ge y$ after interchanging the two residual factors if
necessary (the displayed choice already has $\ell\le q^2/\ell$).  Hence the
witness is normalized and $x$ is genuinely the minimum possible first
denominator.

There is no gap in the stated equivalence.  It does **not** show that the next
gate works when all prime divisors of $q$ are $1$ modulo $3$, and therefore it
does not prove the Erdős--Straus conjecture.

## Verification

Run:

```bash
cd code && bash run.sh
```

The dependency-free checker uses integer arithmetic only.  It:

1. expands the cross-multiplied witness identity in a small exact symbolic
   polynomial ring and checks its reduction by $4x-n-3=0$, $nx-q=0$, and
   $de-q^2=0$;
2. exhaustively checks the first-gate criterion for every $n\equiv1\pmod {12}$
   through $100{,}000$ and rechecks every constructed witness via
   $4xyz=n(xy+yz+zx)$; and
3. confirms the per-class offset-zero counts
   $72,64,70,68,64,59$, totaling $397$ of the $714$ Mordell-class values in
   the parent profile.

The computation is corroborative; the proof above establishes the unbounded
claim.  A counterexample to either implication, or a symbolic mismatch in the
displayed construction, would falsify the claim.

## Open questions

- Apply the three-factor criterion with $r=7$ to characterize offset one in
  terms of signed prime-factor residues modulo $7$.
- Determine whether the successive conditions for $r=3,7,11,\ldots$ admit a
  useful density theorem on each Mordell class.
- Formalize the exact converse (including the valuation normalization) in Lean;
  the prior-art Lean file currently records nearby sufficient and rigidity
  statements rather than this composite-$n$ fixed-gate equivalence.
