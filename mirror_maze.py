from collections import defaultdict

from range_dict import RangeDict


class Mirror:
    def __init__(self, x, y, lean, reflective_on_right, reflective_on_left):
        self.x = x
        self.y = y
        if lean not in ['R', 'L']:
            raise ValueError(f'lean must be one of L or R, but got {lean}')
        self.lean = lean
        self.reflective_on_right = reflective_on_right
        self.reflective_on_left = reflective_on_left


class MirrorMaze:
    def __init__(self, definition_file):
        with open(definition_file, 'r') as file:
            lines = file.read().splitlines()
            self.width, self.height = self.parse_dimensions(lines[0])
            if not self.is_section_separator(lines[1]):
                raise ValueError('Second line of definition file must be section separator (-1).')
            directions = ['U', 'D', 'L', 'R']
            self.reflections = {direction: defaultdict(list) for direction in directions}
            for line in lines[2:-3]:
                mirror = self.parse_mirror(line)
                self.add_mirror(mirror)
            self.sort_reflections()
            if not self.is_section_separator(lines[-3]):
                raise ValueError('Third to last line of definition file must be section separator (-1).')
            self.entry_x, self.entry_y, self.entry_orientation = self.parse_entry(lines[-2])
            if not self.is_section_separator(lines[-1]):
                raise ValueError('Last line of definition file must be section separator (-1).')

    @staticmethod
    def parse_dimensions(line):
        try:
            x, y = line.split(',')
            width = int(x)
            height = int(y)
        except ValueError:
            print('Invalid definition file.  First line must be of the form x,y where x and y are integers.')
            raise
        return width, height

    @staticmethod
    def is_section_separator(line):
        return line == '-1'

    @staticmethod
    def parse_entry(line):
        try:
            x, y_plus = line.split(',')
            entry_x = int(x)
            entry_y = int(y_plus[:-1])
            entry_orientation = y_plus[-1:]
        except ValueError:
            print('Invalid definition file. Laser entry line must be of the form x,yV or x,yH where x and y are '
                  'integers.')
            raise
        return entry_x, entry_y, entry_orientation

    def get_dimensions(self):
        return self.height, self.width

    def get_start_orientation(self):
        return self.entry_x, self.entry_y, self.entry_orientation

    def get_exit_orientation(self):
        x, y = self.entry_x, self.entry_y
        if self.entry_orientation == 'H':
            if x == 0:
                direction = 'R'
                # need to start with x = -1 in order to potentially catch a mirror in the x=0 column
                # this is probably a design smell and ideally some design change would eliminate the hacky correction
                x -= 1
            else:
                direction = 'L'
                # need to start with x = x+1 in order to potentially catch a mirror in the last column
                # this is probably a design smell and ideally some design change would eliminate the hacky correction
                x += 1
        else:
            if y == 0:
                direction = 'U'
                # need to start with y = -1 in order to potentially catch a mirror in the y=0 row
                # this is probably a design smell and ideally some design change would eliminate the hacky correction
                y -= 1
            else:
                direction = 'D'
                # need to start with y = y+1 in order to potentially catch a mirror in the top row
                # this is probably a design smell and ideally some design change would eliminate the hacky correction
                y += 1
        orientation = None
        # previous_steps is looking for a repeated (x, y, direction) tuple which would mean reflections would cycle
        previous_steps = set()
        while orientation is None:
            x, y, direction, orientation = self.get_next_move(x, y, direction)
            if (x, y, direction) in previous_steps:
                raise RuntimeError(f'Stuck in infinite reflection: {x=}, {y=}, {direction=}')
            previous_steps.add((x, y, direction))
        return x, y, orientation

    @staticmethod
    def parse_mirror(line):
        if line[-2] in ['R', 'L']:
            x, y = line[:-2].split(',')
            x = int(x)
            y = int(y)
            lean = line[-2]
            reflective_on_right = line[-1] == 'R'
            reflective_on_left = line[-1] == 'L'
        else:
            x, y = line[:-1].split(',')
            x = int(x)
            y = int(y)
            lean = line[-1]
            reflective_on_right = True
            reflective_on_left = True
        return Mirror(x, y, lean, reflective_on_right, reflective_on_left)

    def add_mirror(self, mirror):
        if mirror.lean == 'L':
            if mirror.reflective_on_left:
                self.reflections['R'][mirror.y].append((mirror.x, 'D'))
                self.reflections['U'][mirror.x].append((mirror.y, 'L'))
            if mirror.reflective_on_right:
                self.reflections['L'][mirror.y].append((mirror.x, 'U'))
                self.reflections['D'][mirror.x].append((mirror.y, 'R'))
        elif mirror.lean == 'R':
            if mirror.reflective_on_left:
                self.reflections['R'][mirror.y].append((mirror.x, 'U'))
                self.reflections['D'][mirror.x].append((mirror.y, 'L'))
            if mirror.reflective_on_right:
                self.reflections['L'][mirror.y].append((mirror.x, 'D'))
                self.reflections['U'][mirror.x].append((mirror.y, 'R'))
        else:
            raise ValueError(f"mirror.lean is not in ['L', 'R'], {mirror.lean=}")

    def sort_reflections(self):
        for direction, direction_dict in self.reflections.items():
            self.reflections[direction] = defaultdict(RangeDict)
            for key, value in direction_dict.items():
                self.reflections[direction][key] = RangeDict(value, increasing=direction in ['U', 'R'])

    def get_next_move(self, x, y, direction):
        # Ideally this code would be simplified to not have different cases for different directions (is that possible?)
        idx, loc = (x, y) if direction in ['U', 'D'] else (y, x)
        # the work of finding the next mirror is mostly being done by RangeDict.find() here
        new_direction = self.reflections[direction][idx].find(loc)
        # I don't like the 2 different return cases for new_direction, but it works.
        # Maybe should raise an exception if no next mirror is found instead?
        if new_direction is None:
            if direction == 'U':
                return x, self.height-1, None, 'V'
            elif direction == 'D':
                return x, 0, None, 'V'
            elif direction == 'L':
                return 0, y, None, 'H'
            else:
                return self.width-1, y, None, 'H'
        else:
            if direction in ['U', 'D']:
                return idx, new_direction[0], new_direction[1], None
            else:
                return new_direction[0], idx, new_direction[1], None
