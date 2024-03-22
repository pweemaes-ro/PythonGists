"""Tests of get_moving_averages."""
from collections.abc import Sequence
from typing import Any

import pytest
from get_moving_averages import get_moving_averages, Number

valid_test_data = [     # data, window_size, expected (inclding incomplete ma's)
	([], 3, []),
	([1], 1, [1]),
	([1, 2], 1, [1, 2]),
	([1, 2], 2, [1.0, 1.5]),
	([1, 2], 3, [1.0, 1.5]),
	([1, 2, 3, 4, 5], 3, [1, 1.5, 2.0, 3.0, 4.0]),
	([1, 2, 3, 4, 5], 4, [1.0, 1.5, 2.0, 2.5, 3.5]),
	([1, 2, 3, 4, 5], 5, [1.0, 1.5, 2.0, 2.5, 3.0]),
	([1, 2, 3, 4, 5], 6, [1.0, 1.5, 2.0, 2.5, 3.0]),
	([1.0, 2, 3.0, 4, 5], 3, [1, 1.5, 2.0, 3.0, 4.0]),
	([-1, -2, -3, -4, -5], 3, [-1.0, -1.5, -2.0, -3.0, -4.0]),
	([-1, -2, -3, -4, -5], 4, [-1.0, -1.5, -2.0, -2.5, -3.5]),
	([-1, -2, -3, -4, -5], 5, [-1.0, -1.5, -2.0, -2.5, -3.0]),
	([-1, -2, -3, -4, -5], 6, [-1.0, -1.5, -2.0, -2.5, -3.0]),
]

invalid_window_size_not_positive: (
	list)[tuple[list[Number], int, list[Number]]] = [
	([], 0, []),                        # window size illegal (must be >= 1)
	([-1, -2, -3, -4, -5], -1, []),     # window size illegal (must be >= 1)
	([1, 2, 3, 4, 5], -1, []),          # window size illegal (must be >= 1)
]

invalid_window_size_float: list[tuple[list[Number], Any, list[Number]]] = [
	([], 0.0, []),                       # window size illegal (must be int)
	([-1, -2, -3, -4, -5], 1.1, []),     # window size illegal (must be int)
	([1, 2, 3, 4, 5], "0.2", []),        # window size illegal (must be int)
]

non_numeric_data: list[tuple[list[Any], int, list[Number]]] = [
	(['1', '2', '3', '4'], 3, []),     # data not numeric
]


@pytest.mark.parametrize("data, window_size, expected", valid_test_data)
def test_get_moving_averages_no_incomplete(data: Sequence[Number],
                                           window_size: int,
                                           expected: Sequence[float]) -> None:
	"""Test get_moving_average function, dont include averages over incomplete
	windows."""
	
	result = get_moving_averages(data, window_size)
	assert result == expected[window_size - 1:]


@pytest.mark.parametrize("data, window_size, expected", valid_test_data)
def test_get_moving_averages_inc_incomplete(data: Sequence[Number],
                                            window_size: int,
                                            expected: Sequence[float]) -> None:
	"""Test get_moving_average function, include averages over incomplete
	windows."""
	
	result = get_moving_averages(data, window_size, include_incomplete=True)
	assert result == expected


@pytest.mark.parametrize("data, window_size, expected",
                         invalid_window_size_not_positive)
def test_get_moving_average_window_size_not_positive(
	data: Sequence[Number],
	window_size: int,
	expected: Sequence[Number]) -> None:
	"""Test get_moving_average function with invalid window size < 1. Should
	raise a value error."""
	
	with pytest.raises(ValueError):
		get_moving_averages(data, window_size)
	
	with pytest.raises(ValueError):
		get_moving_averages(data, window_size, include_incomplete=True)


@pytest.mark.parametrize("data, window_size, expected",
                         invalid_window_size_float)
def test_get_moving_average_window_size_not_int(data: Sequence[Number],
                                                window_size: int,
                                                expected: Sequence[Number]) \
	-> None:
	"""Test get_moving_average function with invalid window size type (not
	int). Should raise a type error."""

	with pytest.raises(TypeError):
		get_moving_averages(data, window_size)

	with pytest.raises(TypeError):
		get_moving_averages(data, window_size, include_incomplete=True)


@pytest.mark.parametrize("data, window_size, expected", non_numeric_data)
def test_get_moving_average_non_numeric_data(data: Sequence[Number],
                                             window_size: int,
                                             expected: Sequence[Number]) \
	-> None:
	"""Test get_moving_average function with invalid data type (not int or
	float). Should raise a type error."""

	with pytest.raises(TypeError):
		get_moving_averages(data, window_size)

	with pytest.raises(TypeError):
		get_moving_averages(data, window_size, include_incomplete=True)
