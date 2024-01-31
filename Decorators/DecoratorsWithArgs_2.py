"""A template for decorator functions with arguments. See also preferred
version NOT using partial function in DecoratorsWithArgs_1."""

# NOTE: No type annotations, could not get it right...
from collections.abc import Callable
from functools import wraps, partial
from typing import ParamSpec, TypeVar, Any

T = TypeVar('T')
P = ParamSpec('P')


def decorator(func: Callable[P, T] | None = None,
              *,
              dec_arg: str = 'default dec arg') \
	-> Callable[[Any], Any]:
	"""The top layer takes the decorator arguments. It stores the parameter
	values and returns the real decorator."""
	
	if func is None:
		print(f"Entered decorator {func=}, {dec_arg=}")
		print(f"Will re-enter via partial({decorator}, {dec_arg=})")
		return partial(decorator, dec_arg=dec_arg)
	else:
		print(f"Entered/re-entered decorator with {func=}, {dec_arg=}")

	@wraps(func)
	def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
		"""The inner most layer is the function wrapping func. This is
		returned by real_decorator."""
		
		print(f"Preprocessing here... ({args=}, {kwargs=})")
		result = func(*args, **kwargs)
		print(f"Postprocessing ({result=})")
		return result
	
	return wrapper
	

# NOTICE:
# For this version to work, the arguments to decorator (other than 'func') MUST
# be supplied as keyword arguments and should therefore be specified as keyword
# arguments in decorator function. (Otherwise the first argument would be
# interpreted as the positional argument 'func').
# NOTICE:
#
# @decorator
# def decorated_func(base: int, exponent: int):
# 	return base ** exponent
#
# WILL WORK if all arguments other than 'func' for 'decorator' have a default
# value. Then this call uses the default value for 'dec_arg', and
# 'decorated_func' is the (first) positional argument 'func' to 'decorator'
# function.
#
# @decorator()
# def decorated_func(base: int, exponent: int):
# 	return base ** exponent
#
# WILL WORK, again using default value for 'dec_arg' and 'decorated_func' as
# (first) positional argument 'func' for partial(decorator, dec_args=dec_arg).
# It is equivalent to providing the default value for dec_arg argument:
#
# @decorator(dec_arg='default dec_arg')
# def decorated_func(base: int, exponent: int):
# 	return base ** exponent

# @decorator
# def decorated_func(base: int, exponent: int) -> int:
# 	"""Simple example func to illustrate the use of decorators. """
#
# 	return int(base ** exponent)
#
#
# # noinspection PyArgumentList
# print(decorated_func(2, exponent=3))
#
# @decorator()
# def decorated_func(base: int, exponent: int) -> int:
# 	"""Simple example func to illustrate the use of decorators. """
#
# 	return int(base ** exponent)
#
#
# # noinspection PyArgumentList
# print(decorated_func(2, exponent=3))
#

@decorator(dec_arg='dec_arg')
def decorated_func(base: int, exponent: int) -> int:
	"""Simple example func to illustrate the use of decorators. """
	
	return int(base ** exponent)


# noinspection PyArgumentList
print(decorated_func(2, exponent=3))

# Here's what's 'really' happening...
# def decorated_func(base: int, *, exponent: int) -> int:
# 	return int(base ** exponent)
#
#
# decorated_func = decorator(dec_arg="dec_arg")(decorated_func)
# print(decorated_func(2, exponent=3))
