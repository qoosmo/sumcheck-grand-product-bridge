# 05 — References and provenance

This project investigates the presentation and cost of a specific Sumcheck-to-vector-Grand-Product encoding. It must not claim to have invented the original Sumcheck protocol, additive-group encodings, module-valued Sumcheck, or conventional Grand Product arguments.

- Lund, Fortnow, Karloff, Nisan, **Algebraic Methods for Interactive Proof Systems**, *JACM* 39(4), 1992. https://doi.org/10.1145/146585.146605
- Bootle, Chiesa, Sotiraki, **Sumcheck Arguments and their Applications**, CRYPTO 2021. https://research.ibm.com/publications/sumcheck-arguments-and-their-applications — module-related Sumcheck prior art.
- Ben-Sasson, Bentov, Horesh, Riabzev, **Fast Reed-Solomon Interactive Oracle Proofs of Proximity**, ICALP 2018. https://doi.org/10.4230/LIPIcs.ICALP.2018.14 — optional low-degree/backend context, **not** part of the algebraic equivalence.
- Earlier project notes (2026-11-17): https://github.com/qoosmo/multilinear-sumcheck/tree/main/docs/derivation-notes/cross-field-sumcheck
- Goldilocks implementation context: https://github.com/0xPolygonZero/plonky2/blob/main/field/src/goldilocks_field.rs

## Priority of research questions

1. Is the equivalence exploitable in a more efficient product-checking architecture?
2. Can the vector product and scalar action constraints be represented with a clean formal security reduction and a real PCS terminal check?
3. Does any performance advantage survive comparison with XOR/parity AIR and existing binary-friendly proving backends?

**Research status:** explorative, not peer-reviewed, and not a claim of cryptographic novelty.
