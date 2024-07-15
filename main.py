from mirror_maze import MirrorMaze

if __name__ == '__main__':
    mirror_maze = MirrorMaze("maze_sample.txt")
    height, width = mirror_maze.get_dimensions()
    print(f'{height=}, {width=}')
    start_x, start_y, start_orientation = mirror_maze.get_start_orientation()
    print(f'{start_x=}, {start_y=}, {start_orientation=}')
    exit_x, exit_y, exit_orientation = mirror_maze.get_exit_orientation()
    print(f'{exit_x=}, {exit_y=}, {exit_orientation=}')
