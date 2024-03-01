"""A class implementation of the same maze (functional version deleted)..."""
from typing import TypeAlias

Location: TypeAlias = tuple[int, int]
Locations: TypeAlias = list[Location]
Path: TypeAlias = dict[Location, int]
NrRightTurns: TypeAlias = int
NrLeftTurns: TypeAlias = int
PathInfo: TypeAlias = tuple[NrRightTurns, NrLeftTurns, Path]

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
__cell_width = 4


class Maze:
	"""A maze as a class..."""
	
	def __init__(self, maze: list[str],
	             start: Location,
	             finish: Location,
	             required: list[list[Location]]) -> None:
		self.maze = maze
		self.start = start
		self.finish = finish
		self.required = required
		self.path_infos: list[PathInfo] = []
	
	def find_all_paths(self,
	                   start: Location | None = None,
	                   path: Path | None = None) -> None:
		""" Find all possible paths from start to finish in the maze."""
		
		start = start or self.start
		path = path or dict()
		
		# Append current start position to the path
		path[start] = len(path.items()) + 1
		
		if start == self.finish:
			if self.is_valid_path(path):
				self.path_infos.append((*self.count_turns(path), path.copy()))
		else:
			x, y = start
			for destination in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
				if self.is_valid_move(destination) and destination not in path:
					self.find_all_paths(destination, path)
		
		# Remove current start position from the path ( => backtrack)
		del path[start]
	
	def is_valid_path(self, path: Path) -> bool:
		"""Return True if all required parts are in the path, else False."""
		
		for r in self.required:
			try:
				index = path[r[0]]
				for i in range(1, len(r)):
					if path[r[i]] != index + i:
						return False
			except KeyError:
				return False
		
		return True
	
	@staticmethod
	def path_to_ordered_locations(path: Path) -> Locations:
		"""Return the path's ordered locations in a list."""
		
		# return tuple(location for (location, index) in
		#         sorted(path.items(), key=lambda item: item[1]))
		return [location for (location, index) in
		        sorted(path.items(), key=lambda item: item[1])]
	
	def count_turns(self, path: Path) -> tuple[NrRightTurns, NrLeftTurns]:
		"""Return tuple of nr of right turns and nr of left turns."""
		
		locations = self.path_to_ordered_locations(path)
		return (self.count_right_turns(locations),
		        self.count_left_turns(locations))
	
	@staticmethod
	def count_right_turns(locations: Locations) -> int:
		"""Return the nr of right turns in the given ordered path."""

		return sum(
			any([prev == (x + 1, y) and dest == (x, y - 1),
			     prev == (x, y + 1) and dest == (x + 1, y),
			     prev == (x - 1, y) and dest == (x, y + 1),
			     prev == (x, y - 1) and dest == (x - 1, y)])
			for prev, (x, y), dest in
				zip(locations, locations[1:], locations[2:]))
	
	@staticmethod
	def count_left_turns(locations: Locations) -> int:
		"""Return the nr of left turns in the given ordered path."""

		return sum(
			any([prev == (x + 1, y) and dest == (x, y + 1),
			     prev == (x, y + 1) and dest == (x - 1, y),
			     prev == (x - 1, y) and dest == (x, y - 1),
			     prev == (x, y - 1) and dest == (x + 1, y)])
			for prev, (x, y), dest in
			zip(locations, locations[1:], locations[2:]))
	
	def is_valid_move(self, destination: Location) -> bool:
		"""Checks if the given coordinates are valid in the maze. Assumes a
		square maze!"""
		
		x, y = destination
		return (0 <= y < len(self.maze) and
		        0 <= x < len(self.maze[0]) and
		        self.maze[y][x] != '#')
	
	def __str__(self) -> str:
		return '\n'.join(self.maze)
	
	def print_path(self, path: Path, cell_width: int) -> None:
		"""Print the path"""
		printable_matrix: list[list[str]] = []
		
		cell_width = max(3, cell_width)
		# Fill with blocks and open spaces
		row_range = range(len(self.maze[0]))
		for y in range(len(self.maze)):
			line = [('█' if self.maze[y][x] == '#' else ' ') * cell_width
			        for x in row_range]
			printable_matrix.append(line)
		
		# Overwrite cells that are on path with the stepnr in the path.
		spaces = cell_width - 2     # idx at most 2 digits
		trailing_spaces = spaces // 2
		leading_spaces = spaces - trailing_spaces
		
		for (x, y), idx in path.items():
			printable_matrix[y][x] = (f"{' ' * leading_spaces}"
			                          f"{idx:=2d}"
			                          f"{' ' * trailing_spaces}")
		
		"""Finally, print the (per line) joined strings in the matrix"""
		for row in printable_matrix:
			print(''.join(row))


if __name__ == "__main__":

	def _main_class() -> None:
		maze = Maze(__a_maze_ing, __start, __finish, __required)
		print(maze)
		maze.find_all_paths()
		for right_turns, left_turns, path in maze.path_infos:
			print(f"Nr of right turns: {right_turns} for following path:")
			print(f"Nr of left turns: {left_turns} for following path:")
			maze.print_path(path, __cell_width)
			print()

	_main_class()
