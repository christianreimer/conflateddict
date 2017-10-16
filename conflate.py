"""
Conflating updates
"""

import collections

ohlc = collections.namedtuple('ohlc', 'open high low close')


class Conflator(object):
    """
    Simple Conflator returning dirty values
    """
    def __init__(self):
        self._data = {}
        self._dirty = set()

    def __str__(self):
        return '<{} dirty:{} entries:{}>'.format(
            self.__class__.__name__, len(self._dirty), len(self._data))

    def __len__(self):
        return len(self._dirty)

    def __iter__(self):
        return iter(self._dirty)

    def __setitem__(self, key, data):
        self._data[key] = data
        self._dirty.add(key)

    def __getitem__(self, key):
        if key in self._dirty:
            return self._data[key]
        raise KeyError('{} not found in dirty set'.format(key))

    def values(self):
        """
        Return iterator over dirty values.
        """
        for key in self._dirty:
            yield self._data[key]

    def keys(self):
        """
        Return iterator over dirty keys.
        """
        return iter(self._dirty)

    def items(self):
        """
        Return iterator over dirty (key, value) tuples.
        """
        for key in self._dirty:
            yield (key, self._data[key])

    def reset(self):
        """
        Resets the Conflator. After calling this there will be no dirty keys.
        """
        self._dirty = set()

    def data(self):
        """
        Return the complete datset.
        """
        return self._data


class OHLCConflator(Conflator):
    """
    Conflator returning OHLC values
    """
    def __init__(self):
        super(OHLCConflator, self).__init__()

    def __setitem__(self, key, data):
        _data = self._data.get(key, None)

        if _data:
            if data > _data.high:
                # New high and new last
                self._data[key] = ohlc(_data.open, data, _data.low, data)
            elif data < _data.low:
                # New low and new last
                self._data[key] = ohlc(_data.open, _data.high, data, data)
            else:
                # New last
                self._data[key] = ohlc(_data.open, _data.high, _data.low, data)
        else:
            # First observation of key
            self._data[key] = ohlc(data, data, data, data)

        self._dirty.add(key)


class MeanConflator(Conflator):
    """
    Conflator returning mean values
    """
    def __init__(self):
        super(MeanConflator, self).__init__()  # pragma: no cover

