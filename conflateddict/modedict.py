from . import conflateddict
import collections


class ModeConflator(conflateddict.ConflatedDict):
    """
    ConflatedDict returning the mode value for a key.
    """

    def __init__(self):
        super(ModeConflator, self).__init__()

    def __setitem__(self, key, data):
        """
        Update the mean value for key and mark key as dirty.
        """
        cnt = self._data.get(key, collections.Counter())
        cnt[data] += 1
        self._data[key] = cnt
        self._dirty.add(key)
    
    def __getitem__(self, key):
        """
        Return the most commonly observed value for key. Raises KeyError if
        key is not dirty.
        """
        if key in self._dirty:
            return self._data[key].most_common(1)[0]
        raise KeyError(f'{key} not found in dirty set')
