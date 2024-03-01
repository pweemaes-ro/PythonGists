"""A class implementation of the same maze..."""
from Common import Maze, Location, PathInfo, Locations, Path, \
	__a_maze_ing, __start, __finish, __required, __cell_width


class RightTurnsMaze:
	"""Same thing, now as a class..."""
	
	def __init__(self, maze: Maze,
	             start: Location,
	             finish: Location,
	             required: list[Locations]) -> None:
		self.maze = maze
		self.start = start
		self.finish = finish
		self.required = required
		self.all_path_infos: list[PathInfo] = []
	
	def find_all_paths(self,
	                   start: Location | None = None,
	                   path: Path | None = None) -> None:
		""" Finds all possible paths from start to finish in the maze."""
		
		if start is None:
			start = self.start
		
		if path is None:
			path = dict()
		
		# Append current start position to the path
		path[start] = len(path.items()) + 1
		
		x, y = start
		if (x, y) == self.finish:
			if self.is_valid_path(path):
				locations = [k for (v, k) in
				             sorted([(v, k) for (k, v) in path.items()])]
				self.all_path_infos.append(
					(self.count_right_turns(locations), locations))
		else:
			for destination in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
				if (self.is_valid_move(destination) and
				destination not in path):
					self.find_all_paths(destination, path)
		
		# Remove current position from the path to backtrack
		del path[(x, y)]
	
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
	
	def print_path(self, locations: Locations, cell_width: int) -> None:
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
		
		for idx, (x, y) in enumerate(locations, start=1):
			printable_matrix[y][x] = (f"{' ' * leading_spaces}"
			                          f"{idx:=2d}"
			                          f"{' ' * trailing_spaces}")
		
		"""Finally, print the (per line) joined strings in the matrix"""
		for row in printable_matrix:
			print(''.join(row))


if __name__ == "__main__":

	def _main_class() -> None:
		maze = RightTurnsMaze(__a_maze_ing, __start, __finish, __required)
		print(maze)
		maze.find_all_paths()
		for turns, path in maze.all_path_infos:
			print(f"Nr of right turns: {turns} for following path:")
			maze.print_path(path, __cell_width)
			print(f"{maze.count_right_turns(path)=}")
			print(f"{maze.count_left_turns(path)=}")
			print()

	_main_class()
