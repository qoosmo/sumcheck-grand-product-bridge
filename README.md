# Sumcheck ↔ Grand Product Bridge

**An additive-to-multiplicative reformulation of Sumcheck across fields**

> **Status (2026-11-17):** mathematical research prototype. The identity and encoded interactive protocol are exact for the specified finite fields. This is **not yet** a competitive Grand Product IOP, polynomial commitment scheme, production prover, or an established novel cryptographic primitive.

## One-sentence idea

Represent the additive group of a characteristic-two extension field by coordinatewise multiplication of sign vectors in an odd-characteristic proving field, so a Sumcheck claim can be read as an **encoded vector Grand Product** claim:

\[
E\!\left(\sum_{x\in\{0,1\}^n} f(x)\right)
= \bigodot_{x\in\{0,1\}^n} E(f(x)).
\]

The symbol `⊙` is **coordinatewise** multiplication, not a scalar Grand Product. The construction is faithful because `E` is injective.

## The bridge in three steps

1. **Fields.** Choose `K = GF(2^k)` (source field) and `P = F_p` for an **odd** prime `p` (e.g. Goldilocks, `p = 2^64 - 2^32 + 1`). Express `a ∈ K` in a fixed `F_2` basis: `a = Σ_j a_j β_j`.
2. **Encoding.** Set `E(a) = ((-1)^{a_0}, …, (-1)^{a_{k-1}}) ∈ {±1}^k ⊂ P^k`. Hence `E(a+b) = E(a) ⊙ E(b)`.
3. **Round interpolation.** For any `r∈K` define `T_r(E(a))=E(ra)` using the binary linear matrix of source-field scalar multiplication. Then

   \[
   E((1-r)a+rb) = T_{1-r}(E(a))\odot T_r(E(b)).
   \]

This supplies **both** a multiplicative Sumcheck round-consistency test and a source-field-correct random-point transition.

## Encoded Sumcheck protocol

For a multilinear polynomial `f∈K[X_1,…,X_n]`, the claim is `h = Σ_{x∈{0,1}^n} f(x)`. The verifier begins with `C_0 = E(h)`.

For `i = 1,…,n`:

1. The prover sends `A_i = E(g_i(0))`, `B_i = E(g_i(1))` where `g_i(t)` is the usual affine Sumcheck partial-sum polynomial.
2. The verifier checks each coordinate is in `{±1}` and `A_i ⊙ B_i = C_{i-1}`.
3. **After** the message, the verifier samples `r_i ← K` uniformly and updates `C_i = T_{1-r_i}(A_i) ⊙ T_{r_i}(B_i)`.

Finally verify `C_n = E(f(r_1,…,r_n))`, with an **authenticated** terminal evaluation. Without this binding, the protocol proves nothing about the intended `f`.

For valid encodings, the round checks decode to ordinary degree-one Sumcheck, and with authenticated evaluation the soundness error for a false claim is at most `n/|K|` (plus the errors of the binding/proving backend). Goldilocks size **does not improve** source-field soundness.

## Why this project exists separately

This repository focuses on the **Sumcheck–Grand Product correspondence** and whether it offers a useful verification architecture. The earlier [cross-field Sumcheck notes](https://github.com/qoosmo/multilinear-sumcheck/tree/main/docs/derivation-notes/cross-field-sumcheck) remain broader notes about module encoding, parity/coefficient extraction, and alternative backends. Nothing in that repository has been moved or changed.

## Start here

- [01 — Algebraic bridge](docs/01-algebraic-bridge.md)
- [02 — Interactive protocol](docs/02-encoded-protocol.md)
- [03 — Soundness, limitations, failure modes](docs/03-soundness-and-limitations.md)
- [04 — Experimental plan and cost model](docs/04-experiments.md)
- [05 — References and provenance](docs/05-references.md)
- [Executable GF(16) toy implementation](examples/toy_gf16.py)

## Run the toy tests

Requires **Python 3.10+**, standard library only:

```bash
python3 -m unittest discover -s tests -v
python3 examples/toy_gf16.py
```

The toy exercises the identities and all encoded protocol rounds using an independently evaluated multilinear extension over `GF(16)`, and includes negative tests. It does **not** measure backend proof time or prove commitment soundness.

## Explicit research question

> Can a faithful additive-to-multiplicative representation turn Sumcheck verification into a *cheaper* Grand Product-style constraint system, once sign membership, scalar actions, terminal evaluation authentication, and realistic source-field security are all paid for?

Do not claim novelty or efficiency before benchmarking against binary-circuit, native-field, and other cross-arithmetic baselines.
