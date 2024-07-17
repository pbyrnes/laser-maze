from bisect import bisect_left, bisect
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
        if not self.keys:
            return None
        if self.increasing and key >= self.keys[-1]:
            return None
        if not self.increasing and key <= self.keys[0]:
            return None
        if self.increasing:
            idx = bisect(self.keys, key)
        else:
            idx = bisect_left(self.keys, key) - 1
        return self.keys[idx], self.values[idx]
