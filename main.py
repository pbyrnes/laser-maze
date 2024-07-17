import argparse

from mirror_maze import MirrorMaze

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="maze definition file", default='maze_sample.txt')
    args = parser.parse_args()
    mirror_maze = MirrorMaze(args.file)
    height, width = mirror_maze.get_dimensions()
    print(f'{height=}, {width=}')
    start_x, start_y, start_orientation = mirror_maze.get_start_orientation()
    print(f'{start_x=}, {start_y=}, {start_orientation=}')
    exit_x, exit_y, exit_orientation = mirror_maze.get_exit_orientation()
    print(f'{exit_x=}, {exit_y=}, {exit_orientation=}')
