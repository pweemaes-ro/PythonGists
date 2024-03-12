"""function to calculate moving averages of a series of data-points."""

from collections import deque
from collections.abc import Sequence
from typing import TypeVar

Number = TypeVar("Number", int, float)


def get_moving_averages(data: Sequence[Number], window_size: int) \
	-> Sequence[float]:
	"""Return a list of moving averages of data. The first ma value is
	calculated over the first window_size datapoints, the last over the last
	window_size datapoints. Therefore the length of the returned list is length
	data - window_size + 1"""
	
	ma = []
	
	if window_size > 0:
		window = deque(data[:window_size - 1], maxlen=window_size)

		for value in data[window_size - 1:]:
			window.append(value)
			ma.append(sum(window) / window_size)
	
	return ma
