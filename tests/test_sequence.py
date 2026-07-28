import unittest
from core.sequence import recaman

class TestRecamanSequence(unittest.TestCase):
    
    EXPECTED_FIRST_12 = [0, 1, 3, 6, 2, 7, 13, 20, 12, 21, 11, 22]

    def test_first_terms(self):
        """Test if the first 12 terms match the canonical sequence."""
        self.assertEqual(recaman(12), self.EXPECTED_FIRST_12)

    def test_step_size_rule(self):
        """Test that the absolute difference between consecutive terms is exactly n."""
        s = recaman(1000)
        for i in range(1, len(s)):
            self.assertEqual(abs(s[i] - s[i-1]), i, 
                             f"Step size failed at n={i}: |{s[i]} - {s[i-1]}| != {i}")

    def test_nonnegative(self):
        """Test that all terms are non-negative."""
        s = recaman(1000)
        self.assertTrue(all(x >= 0 for x in s))

if __name__ == '__main__':
    unittest.main()