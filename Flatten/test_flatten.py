"""Basic tests for flatten module."""
from typing import Any

import pytest

from flatten import flatten, flatten_g


@pytest.fixture
def flatten_input() -> list[Any]:
	"""Input for all tests."""
	
	return [1, 2, [3, 4, 5, ], (6, 7), 8, "abc", ("a", "", 9)]


@pytest.fixture
def expected_output_string_to_chars() -> list[Any]:
	"""Output when string_to_chars is True."""

	return [1, 2, 3, 4, 5, 6, 7, 8, "a", "b", "c", "a", "", 9]


@pytest.fixture()
def expected_output_string_not_to_chars() -> list[Any]:
	"""Output when string_to_chars is False."""

	return [1, 2, 3, 4, 5, 6, 7, 8, "abc", "a", "", 9]


def test_flatten(flatten_input: list[Any],
                 expected_output_string_not_to_chars: list[Any],
                 expected_output_string_to_chars: list[Any]) -> None:
	assert (flatten(flatten_input, str_to_chars=True)
	        == expected_output_string_to_chars)
	assert flatten(flatten_input) == expected_output_string_not_to_chars
	

def test_flatten_g(flatten_input: list[Any],
                   expected_output_string_not_to_chars: list[Any],
                   expected_output_string_to_chars: list[Any]) -> None:

	assert (list(flatten_g(flatten_input, str_to_chars=True))
	        == expected_output_string_to_chars)
	assert list(flatten_g(flatten_input)) == expected_output_string_not_to_chars
