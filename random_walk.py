"""Random walks"""
import random
from math import sqrt, prod
from typing import TypeAlias, Optional

Coordinates: TypeAlias = tuple[int, ...]
Walk: TypeAlias = list[Coordinates]


def _random_walk(dims: int, steps: int, start_location: Coordinates, *,
                 final_destination_only: bool = False) -> Walk:
	"""Return a list of all destinations (if final_destination_only == False)
	or a list with as single item the finale coordinates, after an n-steps
	random walk."""
	
	all_locations = []
	current_location = start_location or tuple(0 for _ in range(dims))
	
	if not final_destination_only:
		all_locations.append(current_location)
	
	for step in range(steps):
		# choose a random dimension along which to move and a random direction
		# to move in.
		dim_delta = random.randrange(dims)
		delta = random.choice([-1, 1])
		
		# update the location by adding delta to the coordinate for the
		# dimension along which to move, leave all other coordinates unchanged.
		current_location = tuple(c + delta if dim == dim_delta else c
		                         for dim, c in enumerate(current_location))
		
		if not final_destination_only:
			all_locations.append(current_location)
	
	return [current_location] if final_destination_only else all_locations


def taxicab_distance(coordinates: Coordinates, *,
                     start_location: Optional[Coordinates] = None) -> int:
	"""Return the taxicab distance to the start_location of the location given
	by coordinates. If no start_location or start_location = None, then the
	origin is used as start location."""
	
	start_location = start_location or tuple(0 for _ in range(len(coordinates)))
	assert len(start_location) == len(coordinates), \
		f"start location has invalid dimension."
	
	return sum(abs(c - s) for c, s in zip(coordinates, start_location))


def euclidean_distance(coordinates: Coordinates, *,
                       start_location: Optional[Coordinates] = None) -> float:
	"""Return the euclidean distance to the start_location of the location
	given by coordinates. If no start_location or start_location = None, then
	the origin is used as start location."""
	
	start_location = start_location or tuple(0 for _ in range(len(coordinates)))
	assert len(start_location) == len(coordinates), \
		f"start location has invalid dimension."
	
	return sqrt(sum((c - s) ** 2 for c, s in zip(coordinates, start_location)))


def random_walk_path(dims: int, steps: int, *,
                     start_location: Optional[Coordinates] = None) -> Walk:
	"""Return list of visited coordinates of n-steps walk. If no start_location
	or start_location = None, then the origin is used as start location."""
	
	start_location = start_location or tuple(0 for _ in range(dims))
	assert len(start_location) == dims
	
	return _random_walk(dims, steps, start_location)


def random_walk_destination(dims: int, steps: int, *,
                            start_location: Optional[Coordinates] = None) \
	-> Coordinates:
	"""Return coordinates of final destination after n-steps random walk. If no
	start_location or start_location = None, then the origin is used as start
	location."""
	
	start_location = start_location or tuple(0 for _ in range(dims))
	assert len(start_location) == dims
	
	return _random_walk(dims, steps, start_location,
	                    final_destination_only=True)[0]


def average_distance(distance_frequencies: dict[int, int]) -> float:
	"""Return the average distance for the given distance frequencies."""
	
	total_distance = sum(map(prod, distance_frequencies.items()))
	nr_walks = sum(distance_frequencies.values())
	return total_distance / nr_walks


def normalize(distance_frequencies: dict[int, int]) -> dict[int, float]:
	"""Return dict with distance and frequency percentage (rounded to 1
	decimal) for all items in distancce_frequencies."""
	
	nr_walks = sum(distance_frequencies.values())
	return {distance: round(frequency * 100 / nr_walks, 1)
	        for distance, frequency in distance_frequencies.items()}


if __name__ == "__main__":
	Distributions: TypeAlias = dict[int, dict[int, int]]
	
	
	def _main() -> None:
		nr_sims = 20_000
		min_n = 10
		max_n = 12
		sim_range = range(nr_sims)
		n_range = range(min_n, max_n + 1, 2)
		max_dist = 4
		
		# distributions: dict[n, frequencies] with
		# 1. n: int = nr of steps in the walk
		# 2. frequencies: dict[distance, frequency] where
		#         1. distance: int = distance reached
		#         2. frequency: int = nr of times any of the n-walks resulted
		#            in a final destination at the given distance.
		# So distributions[3] = {0: 0, 1: 562_000, 2: 0, 3: 438_000} means:
		# 1. n = 3, so each random walk had 3 steps
		# 2. frequencies = {0: 0, 1: 562_000, 2: 0, 3: 438_000}, so
		#    0 walks ended at the origin,
		#    562_000 walks ended at distance 1 from the origing,
		#    0 walks ended at distane 2 from the origin
		#    438_000 walks ended at distance 3 from the origin.
		# The total nr of random walks was therefore 0 + 562_000 + 0 + 438_000
		# = 1_000_000.
		# distributions: dict[int, dict[int, int]] = dict()
		distributions: Distributions = dict()
		
		def _get_perc(max_distance: int, frequencies: dict[int, float]) \
			-> float:
			
			return round(sum(v
			                 for k, v in frequencies.items()
			                 if k <= max_distance), 1)
		
		for n in n_range:
			distributions[n] = {k: 0 for k in range(n + 1)}
			for _ in sim_range:
				d = taxicab_distance(random_walk_destination(dims=2, steps=n))
				distributions[n][d] += 1
			normalized = normalize(distributions[n])
			print(f"{n=:2d}:, {normalized} "
			      f"avg = {average_distance(distributions[n]):4.1f}, "
			      f"perc. d <= {max_dist}: {_get_perc(max_dist, normalized)}")
	
	
	_main()
