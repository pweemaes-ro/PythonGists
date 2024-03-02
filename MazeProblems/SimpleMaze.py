"""A class implementation of the same maze (functional version deleted)..."""
from typing import TypeAlias

Location: TypeAlias = tuple[int, int]
Locations: TypeAlias = tuple[Location, ...]
Path: TypeAlias = dict[Location, int]
TurnsInfo: TypeAlias = tuple[int, int]
PathInfo: TypeAlias = tuple[TurnsInfo, Path]


class Maze:
	"""A maze as a class..."""
	
	def __init__(self, maze: list[str]) -> None:
		self.maze = maze
	
	def find_all_paths(self,
	                   start: Location,
	                   finish: Location,
	                   required: list[Locations]) -> list[PathInfo]:
		""" Find all possible paths from self.current_start to self.finish."""

		def _find_all_paths(current_start: Location, path: Path) -> None:
			"""Recursive! Deals with completing paths from current start to
			finish and putting completed paths in a list, that is eventually
			returned to the caller."""
			
			# Append current current_start position to the path
			path[current_start] = len(path) + 1
			
			if current_start == finish:
				if self.is_valid_path(path, required):
					turns = self.get_nr_right_and_left_turns(path)
					path_infos.append((turns, path.copy()))
			else:
				x, y = current_start
				for dest in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
					if self.is_valid_move(dest) and dest not in path:
						_find_all_paths(dest, path)
			
			# Completed all paths from current start, so backtrack and continu.
			del path[current_start]

		path_infos: list[PathInfo] = []

		_find_all_paths(start, dict())

		return path_infos
		
	@staticmethod
	def is_valid_path(path: Path, required: list[Locations]) -> bool:
		"""Return True if all required paths are in the path, else False."""
	
		for locations in required:
			if (idx := path.get(locations[0], None)) is None:
				return False
			else:
				if not all(path.get(locations[i], None) == idx + i
				           for i in range(1, len(locations))):
					return False

		return True
	
	@staticmethod
	def path_to_ordered_locations(path: Path) -> Locations:
		"""Return the path's ordered locations in a list."""
		
		return tuple(location for (location, index) in
		             sorted(path.items(), key=lambda item: item[1]))
	
	def get_nr_right_and_left_turns(self, path: Path) -> TurnsInfo:
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
			for prev, (x, y), dest
			in zip(locations, locations[1:], locations[2:]))
	
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
		"""Checks if the given coordinates are valid in the maze."""
		
		x, y = destination
		return (0 <= y < len(self.maze) and
				0 <= x < len(self.maze[y]) and
				self.maze[y][x] != '#')
	
	def __str__(self) -> str:
		return '\n'.join(self.maze)
	
	def print_path(self, path: Path, cell_width: int) -> None:
		"""Print the path"""
		
		cell_width = max(3, cell_width)
		lead = ' ' * ((cell_width - 2) // 2)
		trail = ' ' * (cell_width - 2 - len(lead))
		block = '█' * cell_width
		empty = ' ' * cell_width

		printable_matrix = [
			[(lead + f"{path[(x, y)]:=2d}" + trail) if (x, y) in path
			 else block if self.maze[y][x] == '#' else empty
			 for x in range(len(self.maze[y]))]
			for y in range(len(self.maze))]

		"""Finally, print the (per line) joined strings in the matrix"""
		for row in printable_matrix:
			print(''.join(row))
		

if __name__ == "__main__":
	_maze = [
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
	_start = (7, 9)
	_finish = (10, 5)
	_required = [
		((3, 1), (4, 1), (5, 1), (6, 1), (7, 1)),   # → * 5 on line 1
		((6, 3), (6, 4), (6, 5)),                   # ↓ * 3 in lines 3, 4, 5
		((1, 5), (2, 5), (3, 5), (4, 5)),           # → * 4 on line 5 (first)
		((7, 5), (8, 5), (9, 5), (10, 5)),          # → * 4 on line 5 (second)
		((7, 9), (6, 9), (5, 9)),                   # ← * 3 on line 9
	]
	

	def _main_class() -> None:
		maze = Maze(_maze)
		print(maze)
		
		path_infos = maze.find_all_paths(_start, _finish, _required)
		for (right_turns, left_turns), path in path_infos:
			print(f"Nr of right turns: {right_turns} for following path:")
			print(f"Nr of left turns: {left_turns} for following path:")
			maze.print_path(path, cell_width=4)
			print()

	_main_class()
