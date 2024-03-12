from collections.abc import Sequence

import pytest
from get_moving_averages import get_moving_averages, Number


@pytest.mark.parametrize("data, window_size, expected",
		[
			([], 0, []),
			([], 3, []),
			([1], 1, [1]),
			([1, 2], 1, [1, 2]),
			([1, 2], 2, [1.5]),
			([1, 2], 3, []),
			([1, 2, 3, 4, 5], 3, [2.0, 3.0, 4.0]),
			([1, 2, 3, 4, 5], 4, [2.5, 3.5]),
			([1, 2, 3, 4, 5], 5, [3.0]),
			([1, 2, 3, 4, 5], 6, []),
			([1, 2, 3, 4, 5], -1, []),
		]
)
def test_get_moving_averages(data: Sequence[Number],
                             window_size: int,
                             expected: Sequence[float]) -> None:
	"""Test get_moving_average function."""
	
	assert get_moving_averages(data, window_size) == expected
