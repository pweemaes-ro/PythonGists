"""A simulation of the basics of functools.wraps()."""
from collections.abc import Callable
from typing import Any, TypeVar, ParamSpec

T = TypeVar('T')
P = ParamSpec('P')


U = TypeVar('U')
Q = ParamSpec('Q')


def _wraps(func: Callable[P, T]) -> Callable[[Callable[Q, U]], Callable[Q, U]]:
	"""This function mimics the basic behaviour of functools.wraps(). Consider:

	def decorator(func):
		...

		@_wraps(func)
		def wrapper(*args: Any, **kwargs: Any) -> Any:
		...

		return wrapper

	that is, it overwrite some metadata of wrapper function with the metadata
	of the func argument."""
	
	def _decorator(_func: Callable[Q, U]) -> Callable[Q, U]:
		"""The actual decorator function (we need this since _wraps expects an
		argument in its call, before it can handle the wrapped function)."""
		
		def _wrapper(*args: Q.args, **kwargs: Q.kwargs) -> U:
			"""Overwrites some of wrapper's metadata with that of
			wrapped's metadata, and then calls wrapper. Wrapper itself is
			replaced by this function!"""
			
			print(f"Updating metadata of _wrapper from {func.__name__}")
			setattr(_wrapper, "__name__", func.__name__)
			setattr(_wrapper, "__wrapped__", func)
			
			return _func(*args, **kwargs)
		
		return _wrapper
	
	return _decorator


def decorator(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
	"""A sample decorator that uses our own @_wraps to mimic and explain the
	functools.wrap function."""

	print(f"Function being decorated: {func}")

	@_wraps(func)
	def _wrapper(*args: Any, **kwargs: Any) -> Any:
		"""Wrapper around func."""
		
		print(f"Some functionality BEFORE executing {func.__name__} "
		      f"added by decorator...")
		result = func(*args, **kwargs)
		print(f"Some functionality AFTER executing {func.__name__} "
		      f"added by decorator...")
		return result
	
	return _wrapper


@decorator
def add_5(i: int) -> int:
	"""Adds 5 to i and returns result."""
	return i + 5


print(add_5(10))
print(f"{getattr(add_5, '__name__')=}")
_wrapped_func = getattr(add_5, "__wrapped__")
print(f"wrapped add_5 has {_wrapped_func=}")
print(_wrapped_func(42))
print()
