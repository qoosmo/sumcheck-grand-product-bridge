"""GF(16) sign-vector Grand Product / Sumcheck toy (NOT cryptographic).

The GF(16) modulus is x^4 + x + 1. P is the Goldilocks prime.
Only standard-library Python is used.
"""
from __future__ import annotations

from itertools import product
from random import Random

P = (1 << 64) - (1 << 32) + 1
MASK = 0xF
K = 4


def gf_add(a: int, b: int) -> int:
    return a ^ b


def gf_mul(a: int, b: int) -> int:
    """Multiplication modulo the irreducible polynomial x^4+x+1."""
    assert 0 <= a <= MASK and 0 <= b <= MASK
    out = 0
    for _ in range(K):
        if b & 1:
            out ^= a
        b >>= 1
        a <<= 1
        if a & 0x10:
            a ^= 0x13
    return out & MASK


def enc(a: int) -> tuple[int, ...]:
    assert 0 <= a <= MASK
    return tuple(P - 1 if (a >> j) & 1 else 1 for j in range(K))


def valid(u: tuple[int, ...]) -> bool:
    return len(u) == K and all(x in (1, P - 1) for x in u)


def dec(u: tuple[int, ...]) -> int:
    if not valid(u):
        raise ValueError("invalid sign vector")
    return sum((1 << j) for j, x in enumerate(u) if x == P - 1)


def cmul(u: tuple[int, ...], v: tuple[int, ...]) -> tuple[int, ...]:
    if not (valid(u) and valid(v)):
        raise ValueError("invalid sign vector")
    return tuple((x * y) % P for x, y in zip(u, v))


def scalar_action(r: int, u: tuple[int, ...]) -> tuple[int, ...]:
    """T_r(E(a)) using only the binary scalar multiplication matrix."""
    if not valid(u) or not 0 <= r <= MASK:
        raise ValueError("invalid source scalar or sign vector")
    rows = [0] * K
    for i in range(K):
        column = gf_mul(r, 1 << i)
        for j in range(K):
            if (column >> j) & 1:
                rows[j] |= 1 << i
    out = []
    for row in rows:
        value = 1
        for j in range(K):
            if (row >> j) & 1:
                value = (value * u[j]) % P
        out.append(value)
    return tuple(out)


def xor_all(values) -> int:
    out = 0
    for value in values:
        out ^= value
    return out


def mle_from_table(table: dict[tuple[int, ...], int], point: list[int]) -> int:
    """Independent recursive multilinear extension evaluation over GF(16)."""
    n = len(point)
    out = 0
    for bits in product((0, 1), repeat=n):
        weight = 1
        for bit, r in zip(bits, point):
            weight = gf_mul(weight, r if bit else (1 ^ r))
        out ^= gf_mul(weight, table[bits])
    return out


def prove_and_verify(table: dict[tuple[int, ...], int],
                     claimed_sum: int, rng: Random) -> tuple[bool, list[int]]:
    """Simulates the *honest* prover's round polynomials and verifier checks.

    This is NOT an adversarial prover interface or a commitment-opening proof.
    """
    n = len(next(iter(table)))
    if set(table) != set(product((0, 1), repeat=n)):
        raise ValueError("table must contain the entire Boolean cube")
    state = dict(table)
    C = enc(claimed_sum)
    challenges = []
    for remaining in range(n, 0, -1):
        q0 = xor_all(v for b, v in state.items() if b[0] == 0)
        q1 = xor_all(v for b, v in state.items() if b[0] == 1)
        A, B = enc(q0), enc(q1)
        if cmul(A, B) != C:
            return False, challenges
        r = rng.randrange(1 << K)
        challenges.append(r)
        C = cmul(scalar_action(1 ^ r, A), scalar_action(r, B))
        state = {tail: gf_add(gf_mul(1 ^ r, state[(0,) + tail]),
                              gf_mul(r, state[(1,) + tail]))
                 for tail in product((0, 1), repeat=remaining - 1)}
    assert list(state) == [()]
    terminal = mle_from_table(table, challenges)
    return C == enc(terminal) and C == enc(state[()]), challenges


def demo() -> None:
    rng = Random(20261117)
    n = 5
    table = {bits: rng.randrange(16) for bits in product((0, 1), repeat=n)}
    claim = xor_all(table.values())
    ok, challenges = prove_and_verify(table, claim, Random(1729))
    assert ok
    bad, _ = prove_and_verify(table, claim ^ 1, Random(1729))
    assert not bad
    print(f"GF(16) / Goldilocks bridge: {n} rounds PASS")
    print(f"claimed sum: {claim}; challenges: {challenges}")
    print("bad claimed sum: REJECTED")
    print("Not a cryptographic backend or authenticated terminal opening.")


if __name__ == "__main__":
    demo()
