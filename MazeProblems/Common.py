"""Types and example data for maze code."""
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
__cell_width = 4
