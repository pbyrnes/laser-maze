from bisect import bisect_left, bisect
from collections import OrderedDict


class RangeDict:
    '''
    Class to find next mirror.  Initially my hope was this would be a more general data structure, but some of this
    feels specialized to this use case.  Maybe there is an existing Python data structure to use instead (but I didn't
    find one).

    The general idea is to find the next mirror in a direction from a given starting point quickly.
    '''
    def __init__(self, mirror_locations=None, increasing=True):
        if mirror_locations is None:
            mirror_locations = []
        # self.increasing is True if we are going up or right (so indices increase)
        # self.increasing is False if we are going down or left (so indices decrease)
        self.increasing = increasing
        mirror_locations = OrderedDict({k: v for k, v in sorted(mirror_locations)})
        self.keys = list(mirror_locations.keys())
        self.values = list(mirror_locations.values())

    def find(self, key):
        if not self.keys:
            # Returning None if no more mirrors hit feels ugly.  Ideally there would be a unified return structure.
            return None
        if self.increasing and key >= self.keys[-1]:
            # checking if we are already past all the mirrors
            return None
        if not self.increasing and key <= self.keys[0]:
            # checking if we are already past all the mirrors
            return None
        if self.increasing:
            # Figuring out the whether to use bisect or bisect_left and to adjust the index was done mostly by trial
            # and error.  Ideally there would be tests to check various use cases (but I didn't spend the time to write
            # them).
            idx = bisect(self.keys, key)
        else:
            idx = bisect_left(self.keys, key) - 1
        return self.keys[idx], self.values[idx]
