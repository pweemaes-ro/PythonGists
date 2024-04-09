"""If you can avoid it (that is, if data in chainmap is READ ONLY), don't look
up values in the chainmap object, since both 'value = chainmap[key]' and
'chainmap.get(key)' are very slow. Convert the read-only chainmap to dict
first: d = dict(chainmap). Then use value = d[key] or - slightly slower -
value = d.get(key)."""

from timeit import timeit
from collections import ChainMap
from random import choice
from typing import TypeVar, Hashable, MutableMapping, Mapping

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")


def collections_chainmap_to_dict(*maps: MutableMapping[K, V]) -> MutableMapping[
	K, V]:
	"""Uses Python implementation of Collecions.ChainMap(). Is - of course -
	substantially faster than my_chainmap_to_dict."""
	
	return dict(ChainMap(*maps))


def my_chainmap_to_dict(*maps: MutableMapping[K, V]) -> MutableMapping[K, V]:
	"""My implementation of ChainMap(). Is - of course - substantially slower
	than py_chainmap_to_dict."""
	
	retval: MutableMapping[K, V] = dict()
	k_v_generator = ((k, v) for m in maps for (k, v) in m.items())
	
	for (k, v) in k_v_generator:
		retval[k] = retval.get(k, v)
	
	return retval


def lookup_idx(m: Mapping[str, str]) -> None:
	"""Does a lookup using dict[key] syntax."""
	
	for k in range(0, len(m)):
		try:
			_ = m[str(k)]
		except KeyError:
			print(f"invalid key: {k}")
			break


def lookup_get(m: Mapping[str, str]) -> None:
	"""Does a lookup using dict.get(key) method."""
	
	for k in range(0, len(m)):
		try:
			_ = m.get(str(k))
		except KeyError:
			print(f"invalid key: {k}")
			break


def random_string(length: int, chars: str) -> str:
	"""Return a random string of specified length. Each char is the string is
	randomly chosen from chars."""
	
	return ''.join(choice(chars) for _ in range(length))


def create_random_maps(nr_maps: int,
                       nr_items_per_map: int,
                       str_length: int,
                       chars: str) -> list[MutableMapping[str, str]]:
	"""Return a list of nr_maps mutable mappings, each with nr_items_per_map
	items. Keys are integers, values are random strings of 10 chars each."""
	
	maps: list[MutableMapping[str, str]] = []
	nr_maps = max(1, nr_maps)
	nr_items_per_map = max(1, nr_items_per_map)
	
	for map_nr in range(nr_maps):
		_map = dict()
		
		for item_nr in range(nr_items_per_map):
			_map[str(item_nr)] = random_string(str_length, chars)
		
		maps.append(_map)
	
	print(f"created list of {len(maps)} dicts, "
	      f"each with {len(maps[0])} items, "
	      f"each item of length {len(maps[0]['0'])}.")
	
	return maps


if __name__ == "__main__":
	maps_to_chain = create_random_maps(
		nr_maps=10,
		nr_items_per_map=9,
		str_length=8,
		chars="ABC"
	)
	
	funcs = ("collections_chainmap_to_dict",
	         "my_chainmap_to_dict")
	args = ["*maps_to_chain", ]
	for func in funcs:
		for arg in args:
			statement = f"{func}({arg})"
			print(f"{statement:45s}: "
			      f"{timeit(statement, globals=globals(), number=1000):5.2f} "
			      f"secs")
	
	# Init the dicts/chainmap
	dict_from_collections_chainmap = collections_chainmap_to_dict(
		*maps_to_chain)
	dict_from_my_chainmap = my_chainmap_to_dict(*maps_to_chain)
	chainmap = ChainMap(*maps_to_chain)
	
	args = ["dict_from_collections_chainmap",
	        "dict_from_my_chainmap",
	        "chainmap",
	        "dict(chainmap)", ]
	funcs = "lookup_idx", "lookup_get"
	for func in funcs:
		for arg in args:
			statement = f"{func}({arg})"
			print(f"{statement:45s}: "
			      f"{timeit(statement, globals=globals()):5.2f} secs")
	
	# Note: comparing dict to a chainmap means comparing dict to dict(chainmap)
	assert chainmap == dict_from_my_chainmap == dict_from_collections_chainmap
