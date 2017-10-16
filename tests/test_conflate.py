import conflate
import pytest


def test_simple_conflater_value():
    c = conflate.Conflater()
    c[1] = 1
    c[2] = 2
    c[1] = 2
    assert c[1] == 2


def test_simple_conflater_reset():
    c = conflate.Conflater()
    c[1] = 1
    c[2] = 2
    assert c[1] == 1
    c.reset()
    c[1] = 2
    assert c[1] == 2
    with pytest.raises(KeyError):
        c[2]


def test_simple_conflater_len():
    c = conflate.Conflater()
    for i in range(5):
        c[1] = i
        assert len(c) == 1
    c[2] = 1
    assert len(c) == 2
    c.reset()
    assert len(c) == 0
    c[1] = 4
    assert len(c) == 1


def test_simple_conflater_values():
    c = conflate.Conflater()
    for i in range(5):
        c[i] = i
    assert sorted(c.values()) == list(range(5))


def test_simple_conflater_keys():
    c = conflate.Conflater()
    for i in range(5):
        c[i] = i
    assert sorted(c.keys()) == list(range(5))


def test_simple_conflater_items():
    c = conflate.Conflater()
    for i in range(5):
        c[i] = i
    assert sorted(c.items()) == [(i, i) for i in range(5)]


def test_simple_conflater_data():
    c = conflate.Conflater()
    for i in range(5):
        c[i] = i
    data = c.data()
    assert sorted(data.items()) == [(i, i) for i in range(5)]


def test_simple_conflater_str():
    c = conflate.Conflater()
    assert str(c) == '<Conflater dirty:0 entries:0>'
    for i in range(5):
        c[1] = i
    assert str(c) == '<Conflater dirty:1 entries:1>'
    c.reset()
    assert str(c) == '<Conflater dirty:0 entries:1>'


def test_simple_conflater_iter():
    c = conflate.Conflater()
    for i in range(5):
        c[i] = i
    for i, cc in enumerate(c):
        assert cc == i


def test_ohlc_conflater():
    c = conflate.OHLCConflator()
    for i in range(5):
        c[1] = i
    assert c[1] == (0, 4, 0, 4)


def test_ohlc_conflater_high():
    c = conflate.OHLCConflator()
    for i in range(5):
        c[1] = i
    c[1] = 5
    assert c[1] == (0, 5, 0, 5)


def test_ohlc_conflater_low():
    c = conflate.OHLCConflator()
    for i in range(5):
        c[1] = i
    c[1] = -1
    assert c[1] == (0, 4, -1, -1)


def test_ohlc_conflater_last():
    c = conflate.OHLCConflator()
    for i in range(5):
        c[1] = i
    c[1] = 2
    assert c[1] == (0, 4, 0, 2)


def test_ohlc_conflater_str():
    c = conflate.OHLCConflator()
    assert str(c) == '<OHLCConflator dirty:0 entries:0>'
