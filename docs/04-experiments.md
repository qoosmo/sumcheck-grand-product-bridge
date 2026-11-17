# 04 — Experiments, baselines, decision rule

## Hypothesis

A k-coordinate multiplicative representation of `GF(2^k)` could be advantageous if its encoded verification and product relations can be proved more cheaply than conventional binary-circuit or source-field arithmetic under the same Goldilocks backend.

## Baselines on the same workload

- A: encoded Sumcheck via `T_r` and coordinatewise product constraints.
- B: direct Goldilocks boolean/XOR circuit over the `GF(2^k)` evaluation table.
- C: coefficient-extraction / parity AIR, taking advantage of characteristic-two multilinear sum identity.
- D: established Grand Product strategy with an honest cost accounting for vector-valued factors and authentication.

Start with `GF(2^4)` for exhaustive correctness, then `GF(2^16)` with 64 and 256 evaluations. In each case hold constant the commitment and terminal-evaluation interface. A backend comparison must use the *same security target*, which likely requires a substantially larger source challenge field or sound repetition than toy `GF(16)`.

## Report separately

1. Algebraic correctness and negative tests.
2. Number of multiplication, boolean, and sign-membership constraints.
3. Trace width, rows, maximal constraint degree, and quotient polynomial counts.
4. Prover time, verifier time, memory, proof bytes, and security bits **only after implementing a complete backend**.
5. Total soundness error: source sumcheck + commitment/opening + backend.

## Research gates

- G0: prove the algebraic identities (done for stated fields).
- G1: reference toy implementation and negative tests (included; not backend validation).
- G2: correct Goldilocks AIR for sign and `T_r` constraints (open).
- G3: sound terminal evaluation/commitment integration (open).
- G4: fair end-to-end performance comparison (open).

**Continue the line of research only if** an interface advantage, conceptual contribution, or measured performance advantage survives a fair baseline comparison. The group isomorphism alone is not a novelty claim.
