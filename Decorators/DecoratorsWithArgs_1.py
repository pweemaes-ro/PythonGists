"""Preferred template for decorator functions with arguments. See also version
using partial function in DecoratorsWithArgs_2."""
from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar, Any

T = TypeVar('T')
P = ParamSpec('P')


def decorator(dec_arg: Any) -> Callable[[Callable[P, T]], Callable[P, T]]:
	"""The top layer takes the decorator arguments. It stores the parameter
	values and returns the real decorator."""

	print(f"Entered decorator with {dec_arg=}")
	
	def real_decorator(func: Callable[P, T]) -> Callable[P, T]:
		"""The next layer takes th function to wrap"""

		print(f"Entered real_decorator with {func=}")

		@wraps(func)
		def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
			"""The inner most layer is the function wrapping func. This is
			returned by real_decorator."""
			
			print(f"Preprocessing here... ({args=}, {kwargs=})")
			result = func(*args, **kwargs)
			print(f"Postprocessing ({result=})")
			return result
		
		return wrapper
	
	return real_decorator

# NOTICE:
#
# @decorator
# def decorated_func(base: int, exponent: int):
# 	return base ** exponent
#
# print(decorated_func(2, 3))
#
# DOES NOT WORK, since decorator will receive decorator_func as argument, while
# it expects dec_arg. Next, real_decorator is called with arguments that come
# from the call to decorated_func. It is equivalent to:
#
# def decorated_func(base: int, exponent: int):
# 	return base ** exponent
#
# decorated_func = decorator(decorated_func)
# print(decorated_func(2, 3))
#
# NOTICE:
#
# @decorator()
# def decorated_func(base: int, exponent: int):
# 	return base ** exponent
#
# DOES NOT WORK UNLESS the decorator function specifies default values for all
# its arguments.


@decorator('dec_arg')
def decorated_func(base: int, exponent: int) -> int:
	"""Simple example func to illustrate the use of decorators. """

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


print(decorated_func(2, exponent=3))

# Here's what's 'really' happening...
# def decorated_func(base: int, *, exponent: int) -> int:
# 	return int(base ** exponent)
#
#
# decorated_func = decorator("dec_arg")(decorated_func)
# print(decorated_func(2, exponent=3))
