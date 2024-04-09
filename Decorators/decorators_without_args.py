"""A template for a simple decorator function with no arguments (other than the
function it's wrapping of course)."""

from collections.abc import Callable
from functools import wraps
from typing import TypeVar, ParamSpec

T = TypeVar('T')
P = ParamSpec('P')


def decorator(func: Callable[P, T]) -> Callable[P, T]:
	"""The decorator function."""
	
	@wraps(func)
	def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
		"""The function wrapping func."""
		
		print(f"Preprocessing here... ({args=}, {kwargs=})")
		result = func(*args, **kwargs)
		print(f"Postprocessing ({result=})")
		return result
	
	return wrapper


@decorator
def decorated_function(base: int, *, exponent: int) -> int:
	"""Just an example of a function using a decorator. Return base raised to
	the exponent."""
	
	# int() is required since ** has type Any, which causes Mypy to complain:
	# 'error: Returning Any from function declared to return "int".'
	return int(base ** exponent)


# Function definition:
#   def decorated_function(base: int, *, exponent: int) -> int:
# PyCharm inspection:
#   Parameter(s) unfilledPossible callees:(base: int, ..., exponent: int)
# decorated_function.__annotations__:
#   {'base': <class 'int'>, 'exponent': <class 'int'>, 'return': <class 'int'>}
# The problem does NOT occur when the signature of decorated_function is
# changed such that exponent is no longer a keywword-only argument:
#   def decorated_function(base: int, exponent: int) -> int:
#
# noinspection PyArgumentList
print(decorated_function(base=2, exponent=3))
