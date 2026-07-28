from core.sequence import recaman

EXPECTED_FIRST_12 = [0, 1, 3, 6, 2, 7, 13, 20, 12, 21, 11, 22]


def test_first_terms():
    assert recaman(12) == EXPECTED_FIRST_12


def test_no_duplicates():
    s = recaman(1000)
    assert len(s) == len(set(s))


def test_nonnegative():
    s = recaman(1000)
    assert all(x >= 0 for x in s)