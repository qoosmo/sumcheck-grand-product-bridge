# 02 — Interactive encoded Sumcheck

**Public input:** a claim `h∈K`, a commitment or other binding description of a multilinear polynomial `f∈K[X_1,…,X_n]`, a source challenge field `K=GF(2^k)`, and an odd-characteristic constraint field `P`.

**Objective:** verify `h=Σ_{b∈{0,1}^n} f(b)`.

**Assumptions:** one terminal authenticated evaluation `f(r_1,…,r_n)`, fresh independent uniform `r_i∈K` sampled only after round-`i` prover message, correctly enforced sign membership, and correct `T_r` operators.

Initialize `C_0 = E(h)`.

For each `i=1,…,n` the honest prover forms

\[
q_i(X)=\sum_{b\in\{0,1\}^{n-i}} f(r_1,\dots,r_{i-1},X,b).
\]

Because `f` is multilinear, `q_i` is affine in `X`. The prover sends `A_i=E(q_i(0))` and `B_i=E(q_i(1))`.

The verifier checks:

\[
\forall j: (A_i)_j^2=(B_i)_j^2=1,\qquad A_i\odot B_i=C_{i-1}. \tag{3}
\]

It then draws `r_i←K` uniformly and computes

\[
C_i=T_{1-r_i}(A_i)\odot T_{r_i}(B_i). \tag{4}
\]

Finally it checks

\[
C_n=E(f(r_1,\dots,r_n)). \tag{5}
\]

The right side must be provided by a sound polynomial commitment opening or by an independently checked algebraic trace. This document does not implement such authentication.

## Reading (3) as Grand Product

The ordinary sumcheck equation `q_i(0)+q_i(1)=previous_claim` becomes `E(q_i(0))⊙E(q_i(1))=E(previous_claim)`. Recursively, the claimed sum is the vector product of encoded leaf evaluations. Unlike a general-purpose Grand Product IOP, the random transition (4) is derived from the *original affine polynomial*, and cannot be replaced by arbitrary multiplication in `P`.

## Transcript safety

An implementation must enforce `A_i,B_i∈{±1}^k`, sample each challenge after receiving the corresponding message, reject malformed encodings, implement field multiplication matrices exactly, and bind the final evaluation to the same polynomial or trace as the initial statement. When a Fiat–Shamir transform is used, domain separation and transcript binding are additional obligations.
