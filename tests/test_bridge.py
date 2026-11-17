import sys
import unittest
from itertools import product
from pathlib import Path
from random import Random

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'examples'))
from toy_gf16 import (P, gf_add, gf_mul, enc, dec, cmul, scalar_action,
                     valid, xor_all, prove_and_verify, mle_from_table)


class BridgeTests(unittest.TestCase):
    def test_field_multiplication(self):
        self.assertEqual(gf_mul(2, 8), 3)  # x^4 reduces to x+1
        for a in range(1, 16):
            self.assertEqual({gf_mul(a, b) for b in range(16)}, set(range(16)))

    def test_additive_to_multiplicative_exhaustive(self):
        for a in range(16):
            self.assertEqual(dec(enc(a)), a)
            for b in range(16):
                self.assertEqual(enc(gf_add(a, b)), cmul(enc(a), enc(b)))

    def test_scalar_action_exhaustive(self):
        for r in range(16):
            for a in range(16):
                self.assertEqual(scalar_action(r, enc(a)), enc(gf_mul(r, a)))

    def test_affine_interpolation_exhaustive(self):
        for r in range(16):
            for a in range(16):
                for b in range(16):
                    lhs = enc(gf_add(gf_mul(1 ^ r, a), gf_mul(r, b)))
                    rhs = cmul(scalar_action(1 ^ r, enc(a)), scalar_action(r, enc(b)))
                    self.assertEqual(lhs, rhs)

    def test_vector_grand_product(self):
        rng = Random(2006)
        for size in (1, 2, 7, 64):
            vals = [rng.randrange(16) for _ in range(size)]
            out = enc(0)
            for a in vals:
                out = cmul(out, enc(a))
            self.assertEqual(out, enc(xor_all(vals)))

    def test_mle_endpoints(self):
        table = {(a, b, c): (a + 2*b + 4*c) for a,b,c in product((0,1), repeat=3)}
        for bits in table:
            self.assertEqual(mle_from_table(table, list(bits)), table[bits])

    def test_protocol_and_false_claim(self):
        rng = Random(333)
        for n in (1, 2, 3, 5):
            table = {bits: rng.randrange(16) for bits in product((0, 1), repeat=n)}
            claim = xor_all(table.values())
            success, _ = prove_and_verify(table, claim, Random(n))
            failure, _ = prove_and_verify(table, claim ^ 1, Random(n))
            self.assertTrue(success)
            self.assertFalse(failure)

    def test_malformed_sign_vector_rejection(self):
        self.assertFalse(valid((1, 1, 1, 0)))
        self.assertFalse(valid((1, 1, 1, 2)))
        self.assertFalse(valid((1, 1, 1)))
        with self.assertRaises(ValueError):
            dec((1, 1, 1, 0))
        with self.assertRaises(ValueError):
            cmul(enc(3), (1, 1, 1, 0))
        with self.assertRaises(ValueError):
            scalar_action(3, (1, 1, 1, 0))


if __name__ == '__main__':
    unittest.main()
