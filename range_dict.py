from bisect import bisect, bisect_left
from collections import OrderedDict


class RangeDict:
    def __init__(self, d=None, increasing=True):
        if d is None:
            d = {}
        self.increasing = increasing
        d = OrderedDict({k: v for k, v in sorted(d)})
        self.keys = list(d.keys())
        self.values = list(d.values())

    def find(self, key):
        if self.increasing:
            idx = bisect(self.keys, key)
        else:
            idx = bisect_left(self.keys, key)
        try:
            ret_key = self.keys[idx]
            ret_dir = self.values[idx]
        except IndexError:
            return None, None
        return ret_key, ret_dir
