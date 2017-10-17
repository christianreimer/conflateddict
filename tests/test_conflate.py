import conflate
import pytest


def test_simple_conflator_value():
    c = conflate.Conflator()
    c[1] = 1
    c[2] = 2
    c[1] = 2
    assert c[1] == 2


def test_simple_conflator_reset():
    c = conflate.Conflator()
    c[1] = 1
    c[2] = 2
    assert c[1] == 1
    c.reset()
    c[1] = 2
    assert c[1] == 2
    with pytest.raises(KeyError):
        c[2]


def test_simple_conflator_len():
    c = conflate.Conflator()
    for i in range(5):
        c[1] = i
        assert len(c) == 1
    c[2] = 1
    assert len(c) == 2
    c.reset()
    assert len(c) == 0
    c[1] = 4
    assert len(c) == 1


def test_simple_conflator_values():
    c = conflate.Conflator()
    for i in range(5):
        c[i] = i
    assert sorted(c.values()) == list(range(5))


def test_simple_conflator_keys():
    c = conflate.Conflator()
    for i in range(5):
        c[i] = i
    assert sorted(c.keys()) == list(range(5))


def test_simple_conflator_items():
    c = conflate.Conflator()
    for i in range(5):
        c[i] = i
    assert sorted(c.items()) == [(i, i) for i in range(5)]


def test_simple_conflator_data():
    c = conflate.Conflator()
    for i in range(5):
        c[i] = i
    data = c.data()
    assert sorted(data.items()) == [(i, i) for i in range(5)]


def test_simple_conflator_str():
    c = conflate.Conflator()
    assert str(c) == '<Conflator dirty:0 entries:0>'
    for i in range(5):
        c[1] = i
    assert str(c) == '<Conflator dirty:1 entries:1>'
    c.reset()
    assert str(c) == '<Conflator dirty:0 entries:1>'


def test_simple_conflator_iter():
    c = conflate.Conflator()
    for i in range(5):
        c[i] = i
    for i, cc in enumerate(c):
        assert cc == i


def test_simple_conflator_reset_all():
    c = conflate.Conflator()
    for i in range(5):
        c[i] = i
    assert c[1] == 1
    c.clear_all()
    assert not c.data()


def test_timple_conflator_dirty_check():
    c = conflate.Conflator()
    for i in range(5):
        c[i] = i
    for i in range(5):
        assert c.dirty(i)
    c.reset()
    for i in range(5):
        assert not c.dirty(i)


def test_ohlc_conflator():
    c = conflate.OHLCConflator()
    for i in range(5):
        c[1] = i
    assert c[1] == (0, 4, 0, 4)


def test_ohlc_conflator_high():
    c = conflate.OHLCConflator()
    for i in range(5):
        c[1] = i
    c[1] = 5
    assert c[1] == (0, 5, 0, 5)


def test_ohlc_conflator_low():
    c = conflate.OHLCConflator()
    for i in range(5):
        c[1] = i
    c[1] = -1
    assert c[1] == (0, 4, -1, -1)


def test_ohlc_conflator_last():
    c = conflate.OHLCConflator()
    for i in range(5):
        c[1] = i
    c[1] = 2
    assert c[1] == (0, 4, 0, 2)


def test_ohlc_conflator_str():
    c = conflate.OHLCConflator()
    assert str(c) == '<OHLCConflator dirty:0 entries:0>'


def test_mean_conflator():
    c = conflate.MeanConflator()
    c[1] = 1
    c[1] = 2
    c[1] = 3
    assert c[1] == 2
    c.reset()
    c[1] = 5
    assert c[1] == 5


def test_mean_conflator_str():
    c = conflate.MeanConflator()
    assert str(c) == '<MeanConflator dirty:0 entries:0>'


def test_batch_conflator():
    c = conflate.BatchConflator()
    for i in range(5):
        c[1] = i
    assert sorted(c[1]) == list(range(5))
    c.reset()


