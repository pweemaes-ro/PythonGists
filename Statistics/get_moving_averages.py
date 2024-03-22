"""function to calculate moving averages of a series of data-points."""

from collections import deque
from collections.abc import Sequence
from typing import TypeAlias, Union

Number: TypeAlias = Union[int, float]


def get_moving_averages(data: Sequence[Number],
                        window_size: int,
                        include_incomplete: bool = False) -> Sequence[float]:
	"""Return a list of moving averages of data. If include_incomplete is
	False, the first ma value is calculated over the first window_size
	datapoints; if include_incomplete is True, averages for windows of lengths
	1 to window_size - 1 are included. The last average is calculated over the
	last window_size datapoints."""
	
	if not isinstance(window_size, int):
		
		raise TypeError("Window_size must be an int.")
		
	if window_size < 1:
	
		raise ValueError("Window_size must be a positive int.)")
	
	else:
	
		ma = []
	
		window: deque[Number] = deque(maxlen=window_size)
		offset = 0
		
		if not include_incomplete:
			offset = window_size - 1
			window.extend(data[:window_size - 1])
	
		for value in data[offset:]:
			window.append(value)
			ma.append(sum(window) / len(window))
	
		return ma
