"""Find path in maze that has certain required parts and most right turns."""
from typing import TypeAlias


Location: TypeAlias = tuple[int, int]
Locations: TypeAlias = list[Location]
Path: TypeAlias = dict[Location, int]
NrRightTurns: TypeAlias = int
PathInfo: TypeAlias = tuple[NrRightTurns, Locations]
Maze = list[str]

__all_path_infos: list[PathInfo] = []
__a_maze_ing = [
	"#############",
	"#  →→→→→    #",  # → required: (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)
	"# # ### # # #",
	"#     ↓ #   #",  # ↓ required: (6, 3), (6, 4), (6, 5)
	"# ## #↓## # #",
	"#→→→→ ↓→→→F #",  # → required: (1, 5), (2, 5), (3, 5), (4, 5)
	"# ## ## # # #",  # → required: (7, 5), (8, 5), (9, 5), (10, 5)
	"#       # # #",
	"# # # # # # #",
	"#    ←←S    #",  # required: (x, y) = (7, 9), (6, 9), (5, 9)
	"#############",
]
__start = (7, 9)
__finish = (10, 5)
__required = [
	[(3, 1), (4, 1), (5, 1), (6, 1), (7, 1)],  # → * 5 on line 1
	[(6, 3), (6, 4), (6, 5)],  # ↓ * 3 in lines 3, 4, 5
	[(1, 5), (2, 5), (3, 5), (4, 5)],  # → * 4 on line 5 (first)
	[(7, 5), (8, 5), (9, 5), (10, 5)],  # → * 4 on line 5 (second)
	[(7, 9), (6, 9), (5, 9)],  # ← * 3 on line 9
]


def is_valid_move(maze: Maze, destination: Location) -> bool:
	"""Checks if the given coordinates are valid in the maze. Assumes a
	square maze!"""
	
	x, y = destination
	return (0 <= y < len(maze) and
	        0 <= x < len(maze[0]) and
	        maze[y][x] != '#')


def count_right_turns(locations: Locations) -> int:
	"""Return the nr of right turns in the given ordered path."""
	
	return sum(
		any([prev == (x + 1, y) and dest == (x, y - 1),
		     prev == (x, y + 1) and dest == (x + 1, y),
		     prev == (x - 1, y) and dest == (x, y + 1),
		     prev == (x, y - 1) and dest == (x - 1, y)])
		for prev, (x, y), dest in zip(locations, locations[1:], locations[2:]))


def is_valid_path(path: Path) -> bool:
	"""Return True if all required parts are in the path, else False."""

	for r in __required:
		try:
			index = path[r[0]]
			for i in range(1, len(r)):
				if path[r[i]] != index + i:
					return False
		except KeyError:
			return False
	return True


def find_all_paths(maze: Maze,
                   start: Location,
                   finish: Location,
                   path: Path | None = None) -> None:
	""" Finds all possible paths from start to finish in the maze."""
	
	if path is None:
		path = dict()
	
	# Append current start position to the path
	path[start] = len(path.items()) + 1
	
	x, y = start
	if (x, y) == finish:
		if is_valid_path(path):
			locations = [k for (v, k) in
			             sorted([(v, k) for (k, v) in path.items()])]
			__all_path_infos.append((count_right_turns(locations), locations))
	else:
		for destination in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
			if is_valid_move(maze, destination) and destination not in path:
				find_all_paths(maze, destination, finish, path)
	
	# Remove current position from the path to backtrack
	del path[(x, y)]


def print_path(maze: Maze, locations: Locations) -> None:
	"""Print the path"""
	
	printable_matrix: list[list[str]] = []
	
	# Fill with blocks and open spaces
	row_range = range(len(maze[0]))
	for y in range(len(maze)):
		line = [('███' if maze[y][x] == '#' else '   ') for x in row_range]
		printable_matrix.append(line)
	
	# Overwrite open spaces that are on path.
	for idx, (x, y) in enumerate(locations, start=1):
		printable_matrix[y][x] = f"{idx:3d}"
	
	"""Finally, print the (per line) joined strings in the matrix"""
	for row in printable_matrix:
		print(''.join(row))


def print_maze(maze: Maze) -> None:
	"""Print the maze."""
	
	for row in maze:
		print(row)


if __name__ == "__main__":
	
	def _main() -> None:
		print_maze(__a_maze_ing)
		
		find_all_paths(__a_maze_ing, __start, __finish)
		for turns, path in __all_path_infos:
			print(f"Nr of right turns: {turns} for following path:")
			print_path(__a_maze_ing, path)
			print()

	_main()
