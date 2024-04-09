"""A function that recursively flattens a list."""
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
	"""Return a generator that yields all items from list (recurs into
	containers). If str_to_chars == True, strings will also be 'flattened' to
	their individual characters. If str_to_chars == False, strings are
	considered one item each."""
	
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
