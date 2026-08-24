# The chromatic number of the plane (Hadwiger–Nelson problem)

**Slug:** `hadwiger-nelson` · **Area:** discrete-geometry · **Status:** OPEN

## Statement

Let $G$ be the graph whose vertex set is $\mathbb{R}^2$, with an edge between two points exactly when their Euclidean distance is $1$. The **chromatic number of the plane**, written $\chi(\mathbb{R}^2)$, is the least number of colors needed to color all points of the plane so that no two points at distance exactly $1$ receive the same color.

**Question.** What is $\chi(\mathbb{R}^2)$?

Current state: $5 \le \chi(\mathbb{R}^2) \le 7$.

By the de Bruijn–Erdős compactness theorem (which assumes the axiom of choice), $\chi(\mathbb{R}^2)$ equals the maximum chromatic number over all **finite** unit-distance graphs — finite graphs realizable with vertices in the plane and all edges of Euclidean length exactly $1$. So lower bounds reduce to exhibiting finite unit-distance graphs of high chromatic number, which is what makes this problem unusually machine-attackable.

## What counts as progress

- **Resolution:** a proof that $\chi(\mathbb{R}^2) = k$ for some $k \in \{5, 6, 7\}$.
- **$\chi \ge 6$:** a finite unit-distance graph with chromatic number $6$, with verifiable coordinates and a machine-checkable proof of non-5-colorability. This would be a major result.
- **$\chi \le 6$:** a valid $6$-coloring of the plane (e.g. a tiling-based construction with all same-color distances avoiding $1$), with a complete proof.
- **Progress short of that:** smaller 5-chromatic unit-distance graphs than the current record; structural theorems constraining hypothetical 6-chromatic graphs; chromatic numbers of the plane over restricted point sets (subfields, rings); bounds for restricted coloring classes (measurable, tile-based); improved spindle-type constructions; new SAT encodings or symmetry-breaking techniques that materially extend search reach.

## Known results

- **Upper bound 7:** a hexagonal tiling with cell diameter slightly less than $1$, $7$-colored periodically, shows $\chi \le 7$ (construction usually attributed to Isbell, 1950s).
- **Lower bound 4 (classical):** the Moser spindle — a 7-vertex, 11-edge unit-distance graph with $\chi = 4$ (Moser & Moser, 1961).
- **Lower bound 5:** Aubrey de Grey (2018) constructed a 5-chromatic unit-distance graph with 1581 vertices ([arXiv:1804.02385](https://arxiv.org/abs/1804.02385)). The subsequent Polymath16 project and SAT work by Marijn Heule and others reduced the record to graphs with roughly 500–550 vertices, with non-4-colorability certified by SAT solvers producing checkable UNSAT proofs.
- **Rational points:** $\chi(\mathbb{Q}^2) = 2$ (Woodall, 1973). Small algebraic extensions have been studied; the chromatic number over various rings and fields is an active subquestion.
- **Measurable colorings:** if color classes are required to be Lebesgue measurable, at least 5 colors are needed (Falconer, 1981). Under measurability restrictions, the answer can differ from the unrestricted one (Shelah–Soifer), so axioms matter for some variants.
- **Tile-based ("map-type") colorings:** colorings of the plane by regions with reasonable boundaries are known to require at least 6 colors (Townsend; see Soifer's book for the precise statement and history).

## Do not claim

- **Do not claim $\chi \ge 5$ as new.** That is de Grey (2018). A new 5-chromatic graph is only a contribution if it is *smaller* than the current record (~509 vertices; check STATUS.md and existing attempts for the current record known to this repo), or structurally novel in a way you explicitly justify.
- **Finite colorable subgraphs prove nothing upward.** Exhibiting a large unit-distance graph that IS $k$-colorable gives no upper bound on $\chi(\mathbb{R}^2)$.
- **Approximate distances are worthless.** An edge of length $1 \pm 10^{-12}$ under floating point is not an edge. All unit distances must be exact: algebraic coordinates verified symbolically, or verified interval arithmetic proving distance exactly 1 via algebraic identities.
- **Measurable/tile-based bounds do not transfer** to the unrestricted problem. A proof that measurable colorings need 6 colors would be significant but does **not** show $\chi \ge 6$.
- **Beware axiom-of-choice subtleties.** The finite-graph reduction uses AC. State clearly which framework any claim lives in.
- **Probabilistic heuristics, density arguments without rigor, and "the graph looks 6-chromatic" solver runs without certificates are not results.**

## Useful subproblems

- Find 5-chromatic unit-distance graphs with fewer than ~500 vertices (SAT + symmetry breaking; every reduction matters because it shrinks the search space intuition for 6-chromatic candidates).
- Identify structural properties any 6-chromatic unit-distance graph must have (edge density, spindle counts, algebraic degree of coordinates), to prune search.
- Determine $\chi$ of the unit-distance graph over specific fields, e.g. $\mathbb{Q}(\sqrt{3})^2$ or $\mathbb{Q}(\sqrt{2},\sqrt{3})^2$ — concrete, finite-flavor questions with known techniques.
- Improve bounds for the fractional chromatic number of the plane (current best bounds live in the literature — survey and record them here as a `synthesis` attempt first).
- Quantify the trade-off in de Grey-style constructions: which "gadget" families can and cannot be extended to force a 6th color, and why. Rigorous negative results here are valuable `dead-end` attempts.

## Verification requirements

For a claimed $k$-chromatic unit-distance graph (lower-bound claims):

1. **Coordinates:** exact symbolic coordinates (algebraic numbers), or generating code that produces them, for every vertex.
2. **Edge certification:** a script (exact arithmetic — e.g. sympy, or integer arithmetic in a suitable number field) verifying every listed edge has squared distance exactly 1, and stating the edge count.
3. **Non-$(k-1)$-colorability:** a DIMACS CNF encoding of $(k-1)$-colorability, the encoder script, and an UNSAT certificate (DRAT/LRAT) verifiable with a standard checker (`drat-trim`, `cake_lpr`) — or exhaustive-search code with a rigorous argument for its completeness.
4. **$k$-colorability (if claimed):** an explicit coloring, checkable by script.

For upper-bound / coloring claims: the coloring must be described exactly (tile shapes, dimensions, color pattern), with symbolic verification that no color class realizes distance 1 — including tile boundaries, which is where such constructions usually fail.

CI runs `code/run.sh` in each attempt; keep certified artifacts small or provide generation + verification scripts with runtime under ~10 minutes.

## References

- A. Soifer, *The Mathematical Coloring Book*, Springer, 2009 — the standard history and reference for this problem.
- A. de Grey, "The chromatic number of the plane is at least 5", *Geombinatorics* 28 (2018); [arXiv:1804.02385](https://arxiv.org/abs/1804.02385).
- M. Heule's SAT-based reductions of 5-chromatic unit-distance graphs (Geombinatorics, 2018–2021).
- Polymath16 project (2018–2021) on the Hadwiger–Nelson problem.
- Overview: [Wikipedia — Hadwiger–Nelson problem](https://en.wikipedia.org/wiki/Hadwiger%E2%80%93Nelson_problem).
