"""
ConflatedDict

This module contains classes to assist with conflating streaming data. This can
be used to manage the load on conuming tasks, and is especially useful if the
consumers only need the current value and can thus safely discard intermediate
updates.

ConflatedDict - Basic ConflatedDict will only return the most recent value.

OHLCConflator - ConflatedDict will return the Open, High, Low, and Close
values obsered during the interval.

MeanConflator - ConflatedDict will return the mean of the values observed
during the interval.

BatchConflator - ConflatedDict will return all the values (in a batch)
observed during the interval.

LambdaConflator - ConflatedDict that takes a user provided function of the
form f(v, vl) -> cv where v is the current value and vl is the list of past
values observed during the interval and returns the conflated value cv.
"""

import collections

ohlc = collections.namedtuple('ohlc', 'open high low close')


class ConflatedDict(object):
    """
    Simple ConflatedDict returning dirty values
    """

    def __init__(self):
        """
        Initialize ConflatedDict with empty dataset and no dirty keys.
        """
        self._data = {}
        self._dirty = set()

    def __str__(self):
        """
        Return decription of the ConflatedDict
        """
        return '<{} dirty:{} entries:{}>'.format(
            self.__class__.__name__, len(self._dirty), len(self._data))

    def __len__(self):
        """
        Return the number of dirty keys.
        """
        return len(self._dirty)

    def __iter__(self):
        """
        Return iterater over dirty keys.
        """
        return iter(self._dirty)

    def __setitem__(self, key, data):
        """
        Set (or update) the value of key to be equal to data and mark key
        as being dirty.
        """
        self._data[key] = data
        self._dirty.add(key)

    def __getitem__(self, key):
        """
        Return the stored value for key. Raises KeyError if key is not dirty.
        """
        if key in self._dirty:
            return self._data[key]
        raise KeyError('{} not found in dirty set'.format(key))

    def __contains__(self, key):
        """
        Return true if key is dirty.
        """
        return key in self._dirty

    def __delitem__(self, key):
        """
        Delete key and value from internal datastores. Raises KeyError
        if key is not dirty.
        """
        if key not in self._dirty:
            raise KeyError(key)
        self._dirty.remove(key)
        del self._data[key]

    def dirty(self, key):
        """
        Return True if the key is dirty.
        """
        return self.__contains__(key)

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
        Resets dirty map. After calling this there will be no dirty keys.
        """
        self._dirty.clear()
        if hasattr(self, 'additional_reset'):
            self.additional_reset()

    def clear(self):
        """
        Clear out all the data in the ConflatedDict.
        """
        self._dirty.clear()
        self._data.clear()

    def data(self):
        """
        Return the complete datset.
        """
        return self._data


class OHLCConflator(ConflatedDict):
    """
    ConflatedDict returning Open, High, Lown, and Close (Last) values
    """

    def __init__(self):
        super(OHLCConflator, self).__init__()

    def __setitem__(self, key, data):
        """
        Set one or more of the Open, High, Low, Close values for key
        depending on the value of data. Close will always be updated.
        """
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


class MeanConflator(ConflatedDict):
    """
    ConflatedDict returning mean values
    """

    def __init__(self):
        super(MeanConflator, self).__init__()
        self._raw = {}

    def __setitem__(self, key, data):
        """
        Update the mean value for key and mark key as dirty.
        """
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
        self._raw.clear()


class BatchConflator(ConflatedDict):
    """
    ConflatedDict that batches values
    """

    def __init__(self):
        super(BatchConflator, self).__init__()

    def __setitem__(self, key, data):
        """
        Append data to the batch of values for key and mark key as dirty.
        """
        if key not in self._dirty:
            # This is the first time (in this inverval) that we see this key,
            # so we need to clear out the data for this key
            _data = []
        else:
            _data = self._data[key]

        _data.append(data)
        self._data[key] = _data
        self._dirty.add(key)


class LambdaConflator(ConflatedDict):
    """
    ConflatedDict which conflates based on a user provided function
    """

    def __init__(self, f_conf=lambda x, y: x, name=None):
        """
        Initialize LambdaConflator. The argument f_conf must be a function
        of the format `lambda x, y: return z` where x is the current value
        (when updating the conflator), y is the list of past values
        observed for this key (since the last reset), and z is the desired
        conflated value.
        """

        super(LambdaConflator, self).__init__()
        self._f_conf = f_conf
        self._raw = {}
        self._name = name

    def __setitem__(self, key, value):
        """
        Set value of key to be the result of calling the passed in conflator
        with value and the list of values previousely observed for key. Also
        marks key as dirty.
        """
        _raw = self._raw.get(key, [])
        self._data[key] = self._f_conf(value, _raw)
        self._dirty.add(key)
        _raw.append(value)
        self._raw[key] = _raw

    def __str__(self):
        return '<{} dirty:{} entries:{}>'.format(
            self._name and self._name or self.__class__.__name__,
            len(self._dirty), len(self._data))

    def additional_reset(self):
        """
        Resets the raw data to ensure a new mean is calculate for the next
        interval.
        """
        self._raw.clear()
