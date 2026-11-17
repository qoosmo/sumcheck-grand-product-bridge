# 03 — Soundness, limits, and nonclaims

## Correctness theorem

For `K=GF(2^k)` and `P` of odd characteristic, the map `E` defined in [01](01-algebraic-bridge.md) is an injective additive-group homomorphism. The operators `T_r` satisfy `T_r(E(a))=E(ra)`.

**Completeness:** With an honest prover, equations (3)–(5) of [02](02-encoded-protocol.md) hold because `E` preserves addition and `T_r` transports source scalar multiplication.

**Soundness reduction:** Every valid sign vector uniquely decodes to `K`; the verifier's (3) and (4) are *exactly* ordinary degree-one sumcheck equations under this decoding. Therefore, with independently and uniformly sampled `r_i∈K`, an authenticated terminal evaluation, and the standard sumcheck assumptions, a false sum is accepted with probability at most `n/|K|`. Add error from the terminal commitment/backend and any transcript/encoding soundness losses in the actual system.

For a toy `GF(256)` challenge field this is `n/256` (often weak). Choosing Goldilocks as the constraint field does not change the root-counting bound, which is governed by `K`.

## What this result does not prove

1. No ring/field embedding `K→P` exists in differing characteristics, and none is claimed.
2. `G_i(t)=E(q_i(t))` is **not** ordinarily a low-degree `P`-polynomial. Standard `P`-field Grand Product/sumcheck soundness arguments cannot be transplanted unmodified.
3. Equation (1) is a product identity, not by itself a binding commitment or a constant-size Grand Product protocol.
4. Authenticated terminal evaluation, correct scalar actions, sign constraints, and transcript rules are necessary. Without them, prover messages can be fabricated to fit a false claim.
5. Repetition over the same small field might improve error if independently composed and properly bound, but it incurs cost and requires a full argument; using larger source-field extensions is the clearer initial path.
6. For nonfields (especially rings with zero divisors), standard degree-vs-root bounds are not valid without separate analysis.
7. Arithmetic costs can dominate: for `k`-bit extension fields, the direct `T_r` matrix method takes up to `O(k²)` products per action. Packing and PCS integration are open.
8. In characteristic two, the Boolean cube sum of a multilinear polynomial equals the top multilinear coefficient. Direct coefficient-extraction may beat the bridge for this particular statement, but only with a sound coefficient/evaluation binding.

## Suggested attack and validation cases

- False initial claimed sum: must reject except for the stated statistical error.
- Invalid sign vector (`0`, `2`, etc.): must reject even if an equation accidentally passes.
- Corrupted `T_r` action/matrix: must be detected by independent field reference tests.
- Biased/predictable challenges, especially sampled before the prover sends `A_i,B_i`: invalid security model.
- Fake terminal evaluation: should never be accepted solely because the prover supplied it.
- Wraparound or unconstrained conversion when implementing the source extension field in `P`: require explicit enforcement.

The included Python demo checks algebra and local verifier logic; it is **not** a cryptographic security test or a STARK implementation.
