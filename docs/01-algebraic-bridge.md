# 01 — Exact algebraic bridge

Let `K = F_{2^k}` and `P = F_p` with `p` odd. Choose an `F_2`-basis `β_0,…,β_{k-1}` for `K`. Every `a ∈ K` has unique bits `a_j` such that `a=Σ_j a_j β_j`.

Define

\[
E(a)=((-1)^{a_0},\dots,(-1)^{a_{k-1}})\in (P^\times)^k.
\]

Since addition in `K` is bitwise XOR, and `(-1)^{u⊕v}=(-1)^u(-1)^v` for `u,v ∈ {0,1}`,

\[
E(a+b)=E(a)\odot E(b),\qquad
E(0)=(1,\dots,1).
\]

`E` is injective because `+1` and `-1` are distinct in odd characteristic. It is a homomorphism of **additive groups** into a direct product of multiplicative groups. It is **not** a field/ring homomorphism and does not preserve multiplication of arbitrary elements of `K`.

For finite Boolean set `H={0,1}^n` and `f:H→K`, induction gives

\[
E\left(\sum_{x\in H} f(x)\right)
=\bigodot_{x\in H} E(f(x)). \tag{1}
\]

Equation (1) is the advertised Sumcheck ↔ Grand Product identity. Each of the `k` sign coordinates has its own ordinary product. Hence the product is **vector-valued** (or `k` products), and a generic scalar Grand Product protocol does not automatically apply.

## Affine interpolation across fields

For each scalar `r∈K`, multiplication `m_r:a↦ra` is an `F_2`-linear operator with matrix `M_r∈F_2^{k×k}`. Define `T_r` on *valid sign vectors* by

\[
\big(T_r(u)\big)_j=\prod_{\ell:\,(M_r)_{j\ell}=1}u_\ell.
\]

Thus `T_r(E(a))=E(ra)`. Let `a,b∈K`. Since `K` is characteristic two,

\[
\boxed{E((1-r)a+rb)=T_{1-r}(E(a))\odot T_r(E(b)).} \tag{2}
\]

Equation (2) preserves the specific affine interpolation Sumcheck needs. A sign coordinate interpreted as a function of `r` is **not** in general a degree-one polynomial over `P`; source-field interpolation is implemented by `T_r`, not by `(1-r)A+rB` over `P`.

## Costs and constraints

- `k` sign coordinates per source element.
- Sign-validity constraints `u_j^2=1` for each coordinate over `P`.
- Naive generic `T_r` costs up to `O(k^2)` coordinate multiplications, plus elementwise products; more detailed gate counts depend on the scalar multiplication matrices and backend.
- `r` is a source-field random challenge. A Goldilocks verifier circuit needs a correct, bound representation of `r` and its induced matrix, or a commitment/transcript-compatible alternative.
- A direct product scan over `N` entries costs roughly `k(N−1)` coordinate multiplies before proof-system overhead; a specialized proof of these products may offer different trade-offs but is not constructed here.

## Important special case

For multilinear `f` over `K` of characteristic two, its Boolean-hypercube sum is the coefficient of `X_1…X_n`. This may enable a *coefficient-extraction* baseline that is cheaper than either a generic Sumcheck or a Grand Product computation. It must be benchmarked; the top coefficient must be authenticated.
