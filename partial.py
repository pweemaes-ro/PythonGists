"""A python implementation of functools.partial, just to illustrate the
concept."""
from collections.abc import Callable
from functools import wraps, partial
from typing import TypeVar, ParamSpec


T = TypeVar('T')
P = ParamSpec('P')


def my_partial(func: Callable[..., T], /, *args: P.args, **kwargs: P.kwargs) \
	-> Callable[..., T]:
	"""Return a partial function."""
	
	# Not sure about type annotations here, but Mypy (in strictest mode) seems
	# happy. The ellipses mean 'unspecified'. Notice that [Any] won't do, since
	# this implies exactly ONE argument.
	
	@wraps(func)
	def _partial(*pargs: P.args, **pkwargs: P.kwargs) -> T:
		
		# Check if any of the pkwargs passed to _partial was already in 'fixed'
		# arguments kwargs passed to my_partial:"""
		for pkwarg in pkwargs.keys():
			if pkwarg in kwargs.keys():
				raise TypeError(f"Invalid argument {pkwarg!r}: already has "
				                  f"fixed value {kwargs[pkwarg]!r} from call "
				                  f"to {my_partial.__qualname__}.")
		return func(*args, *pargs, **{**pkwargs, **kwargs})
	
	return _partial


def my_function(key: str, count: int, posix: str,
                *,
                useless: str = "NOUseless", extra: str = "NOEXtra") -> None:
	"""Example function, prints all its arguments."""

	print(f"{key=}, {count=}, {posix=}, {useless=}, {extra=}")


fixed_key_func = my_partial(my_function, key='a', count=10, posix="QQQ")
fixed_key_func(extra="Xtra")

py_f = partial(my_function('a'))