"""
Conflate

This module contains classes to assist with conflating streaming data. This can
be used to manage the load on conuming tasks, and is especially useful if the
consumers only need the current value and can thus safely discard intermediate
updates.

Conflator - Basic conflator that will only return the most recent value.

OHLCConflator - Conflator that will return the Open, High, Low, and Close
values obsered during the interval.

MeanConflator - Conflator that will return the mean of the values observed
during the interval.

BatchConflator - Conflator that will return all the values (in a batch)
observed during the interval.
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

    def dirty(self, key):
        """
        Return True if the key is dirty.
        """
        return key in self._dirty

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
        if hasattr(self, 'additional_reset'):
            self.additional_reset()

    def clear_all(self):
        """
        Clear out all the data in the conflator.
        """
        self.reset()
        self._data = {}

    def data(self):
        """
        Return the complete datset.
        """
        return self._data


class OHLCConflator(Conflator):
    """
    Conflator returning Open, High, Lown, and Close (Last) values
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
        self._raw = {}

    def __setitem__(self, key, data):
        val, count = self._raw.get(key, (0, 0))
        val += data
        count += 1
        self._raw[key] = (val, count)
        self._data[key] = val / count
        self._dirty.add(key)

    def additional_reset(self):
        """
        Resets the raw data to ensure a new mean is calculate for the next
        interval.
        """
        self._raw = {}


class BatchConflator(Conflator):
    """
    Conflator that batches values
    """
    def __init__(self):
        super(BatchConflator, self).__init__()

    def __setitem__(self, key, data):
        if key not in self._dirty:
            # This is the first time (in this inverval) that we see this key,
            # so we need to clear out the data for this key
            _data = []
        else:
            _data = self._data[key]

        _data.append(data)
        self._data[key] = _data
        self._dirty.add(key)
