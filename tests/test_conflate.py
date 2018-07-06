import conflateddict
import pytest
import random

def test_simple_conflator_value():
    c = conflateddict.ConflatedDict()
    c[1] = 1
    c[2] = 2
    c[1] = 2
    assert c[1] == 2


def test_simple_conflator_reset():
    c = conflateddict.ConflatedDict()
    c[1] = 1
    c[2] = 2
    assert c[1] == 1
    c.reset()
    c[1] = 2
    assert c[1] == 2
    with pytest.raises(KeyError):
        c[2]


def test_simple_conflator_len():
    c = conflateddict.ConflatedDict()
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
    c = conflateddict.ConflatedDict()
    for i in range(5):
        c[i] = i
    assert sorted(c.values()) == list(range(5))


def test_simple_conflator_keys():
    c = conflateddict.ConflatedDict()
    for i in range(5):
        c[i] = i
    assert sorted(c.keys()) == list(range(5))


def test_simple_conflator_items():
    c = conflateddict.ConflatedDict()
    for i in range(5):
        c[i] = i
    assert sorted(c.items()) == [(i, i) for i in range(5)]


def test_simple_conflator_data():
    c = conflateddict.ConflatedDict()
    for i in range(5):
        c[i] = i
    data = c.data()
    assert sorted(data.items()) == [(i, i) for i in range(5)]


def test_simple_conflator_str():
    c = conflateddict.ConflatedDict()
    assert str(c) == '<ConflatedDict dirty:0 entries:0>'
    for i in range(5):
        c[1] = i
    assert str(c) == '<ConflatedDict dirty:1 entries:1>'
    c.reset()
    assert str(c) == '<ConflatedDict dirty:0 entries:1>'


def test_simple_conflator_iter():
    c = conflateddict.ConflatedDict()
    for i in range(5):
        c[i] = i
    for i, cc in enumerate(c):
        assert cc == i


def test_simple_conflator_reset_all():
    c = conflateddict.ConflatedDict()
    for i in range(5):
        c[i] = i
    assert c[1] == 1
    c.clear()
    assert not c.data()


def test_simple_conflator_dirty_check():
    c = conflateddict.ConflatedDict()
    for i in range(5):
        c[i] = i
    for i in range(5):
        assert c.dirty(i)
    c.reset()
    for i in range(5):
        assert not c.dirty(i)


def test_simple_conflator_delitem():
    c = conflateddict.ConflatedDict()
    for i in range(5):
        c[i] = i

    del c[1]
    assert sorted(c.keys()) == [0, 2, 3, 4]


def test_simple_conflator_delitem_keyerror():
    c = conflateddict.ConflatedDict()
    for i in range(5):
        c[i] = i
    with pytest.raises(KeyError):
        del c['hello']


def test_ohlc_conflator():
    c = conflateddict.OHLCConflator()
    for i in range(5):
        c[1] = i
    assert c[1] == (0, 4, 0, 4)


def test_ohlc_conflator_high():
    c = conflateddict.OHLCConflator()
    for i in range(5):
        c[1] = i
    c[1] = 5
    assert c[1] == (0, 5, 0, 5)


def test_ohlc_conflator_low():
    c = conflateddict.OHLCConflator()
    for i in range(5):
        c[1] = i
    c[1] = -1
    assert c[1] == (0, 4, -1, -1)


def test_ohlc_conflator_close():
    c = conflateddict.OHLCConflator()
    for i in range(5):
        c[1] = i
    c[1] = 2
    assert c[1] == (0, 4, 0, 2)


def test_ohlc_conflator_str_clean():
    c = conflateddict.OHLCConflator()
    assert str(c) == '<OHLCConflator dirty:0 entries:0>'


def test_ohlc_conflator_str_dirty():
    c = conflateddict.OHLCConflator()
    for i in range(random.randint(1, 10)):
        c[i] = i
    expected_str = '<OHLCConflator dirty:{dirty} entries:{entries}>'.format(
        dirty=i+1, entries=i+1)
    assert str(c) == expected_str


def test_mean_conflator():
    c = conflateddict.MeanConflator()
    c[1] = 1
    c[1] = 2
    c[1] = 3
    assert c[1] == 2
    c.reset()
    c[1] = 5
    assert c[1] == 5


def test_mean_conflator_float():
    c = conflateddict.MeanConflator()
    c[1] = 1.0
    c[1] = 2.0
    c[1] = 3.0
    assert c[1] == 2.0
    c.reset()
    c[1] = 5.0
    assert c[1] == 5.0


def test_mean_conflator_strings():
    c = conflateddict.MeanConflator()
    with pytest.raises(TypeError):
        c[1] = 'Hello'


def test_mean_conflator_str_clean():
    c = conflateddict.MeanConflator()
    assert str(c) == '<MeanConflator dirty:0 entries:0>'


def test_mean_conflator_str_dirty():
    c = conflateddict.MeanConflator()
    for i in range(random.randint(1, 10)):
        c[i] = i
    expected_str = '<MeanConflator dirty:{dirty} entries:{entries}>'.format(
        dirty=i+1, entries=i+1)
    assert str(c) == expected_str


def test_batch_conflator():
    c = conflateddict.BatchConflator()
    for i in range(5):
        c[1] = i
    assert sorted(c[1]) == list(range(5))
    c.reset()


def test_lambda_conflator():
    c = conflateddict.LambdaConflator(lambda x, y: x + sum(y))
    c[1] = 1
    assert c[1] == 1
    c[1] = 2
    assert c[1] == 3
    c[1] = 3
    assert c[1] == 6
    c.reset()
    c[1] = 1
    assert c[1] == 1


def test_lambda_conflator_str_clean():
    c = conflateddict.LambdaConflator(lambda x, y: x + sum(y))
    assert str(c) == '<LambdaConflator dirty:0 entries:0>'


def test_lambda_conflator_str_dirty():
    c = conflateddict.LambdaConflator(lambda x, y: x + sum(y))
    for i in range(random.randint(1, 10)):
        c[i] = 1
    expected_str = '<LambdaConflator dirty:{dirty} entries:{entries}>'.format(
        dirty=i+1, entries=i+1)
    assert str(c) == expected_str


def test_lambda_conflator_name():
    n = 'MyName'
    c = conflateddict.LambdaConflator(lambda x, y: x + sum(y), n)
    assert str(c) == '<{} dirty:{} entries:{}>'.format(n, 0, 0)


def test_lambda_conflator_default_args():
    lc = conflateddict.LambdaConflator()
    dc = conflateddict.ConflatedDict()

    for i in range(10):
        key = i % 3
        lc[key] = i
        dc[key] = i
        assert lc[key] == dc[key]


def test_mode_conflator():
    c = conflateddict.ModeConflator()
    c['key'] = 1
    c['key'] = 2
    c['key'] = 2
    c['key'] = 3
    c['key'] = 3
    c['key'] = 3
    assert c['key'] == (3, 3)
    c['key'] = 1
    c['key'] = 1
    c['key'] = 1
    assert c['key'] == (1, 4)


def test_mode_conflator_key_not_found():
    c = conflateddict.ModeConflator()
    c['key'] = 1
    with pytest.raises(KeyError):
        c['key that does not exist']


def test_mode_conflator_name():
    c = conflateddict.ModeConflator()
    assert str(c) == '<ModeConflator dirty:{} entries:{}>'.format(0, 0)
