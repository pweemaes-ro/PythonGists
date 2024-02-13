"""A function that recursively flattens to a list of returns a generator."""
from collections.abc import Iterable, Generator
from typing import Any


def flatten(lst: Iterable[Any], str_to_chars: bool = False) -> list[Any]:
	"""Return a list with all items from lst (recurs into containers). If
	str_to_chars == True, strings will also be 'flattened' to their individual
	characters. If str_to_chars == False, strings are considered one item each.
	"""

	return list(flatten_g(lst, str_to_chars=str_to_chars))


def flatten_g(lst: Iterable[Any], str_to_chars: bool = False) \
	-> Generator[Any, None, None]:
	"""Return a generator that yields all items recursively. If str_to_chars
	== True, strings will also be 'flattened' to their individual characters.
	If str_to_chars == False, strings are considered one item each."""
	
	for item in lst:
		try:
			if iter(item):
				if isinstance(item, str):
					if not str_to_chars or len(item) == 1:
						yield item
					else:
						# Yield from string will generate the chars. No need to
						# call flatten on a string, since strings cannot
						# contain other containers.
						yield from item
				else:
					yield from flatten(item)
		except TypeError:
			yield item


if __name__ == "__main__":
	
	input_data = [1, 2, [3, 4, 5,], (6, 7), 8, "abc", ("a", "", 9)]
	expected_true = [1, 2, 3, 4, 5, 6, 7, 8, "a", "b", "c", "a", "", 9]
	expected_false = [1, 2, 3, 4, 5, 6, 7, 8, "abc", "a", "", 9]
	
	def _test_flatten() -> None:
		assert flatten(input_data, str_to_chars=True) == expected_true
		assert flatten(input_data) == expected_false
		print("_test_flatten() OK")
	
	def _test_flatten_g() -> None:
		g_true = flatten_g(input_data, str_to_chars=True)
		g_false = flatten_g(input_data)
		
		assert list(g_true) == expected_true
		assert list(g_false) == expected_false
		print("_test_flatten_g() OK")

	_test_flatten()
	_test_flatten_g()
