"""Some decorator stuff... Does not (yet) include class decorators."""
from collections.abc import Callable
from functools import partial, wraps
from random import randint
from typing import Any


def retry(func: Any = None, nr: int = 3) -> Callable[[Any], Any]:
	"""One way of supporting arguments for decorator functions... This does
	however requires an optional keyword argument.
	@retry()        # works, uses default value for nr.
	@retry(nr=5)    # works, uses specified value for nr.
	@retry(5)       # does NOT work, since now 5 is interpreted as func arg.
	@retry          # works, decorated function is func argument, nr gets
					# default value.
	See also new_retry function below."""
	
	if func is None:
		return partial(retry, nr=nr)
	
	print(f"Retry decorator for {func.__name__:10s} with {nr} tries.")
	
	@wraps(func)
	def wrapper(*args: Any, **kwargs: Any) -> Any:
		"""The wrapper around func."""
		
		# We use an attribute on the retry function to create state, where we
		# store the total nr of tries for all wrapped functions.
		attr_name = "try_count"
		
		retries_left = nr
		while retries_left > 0:
			try:
				result = func(*args, **kwargs)
				print(f"{func.__name__:10s}: "
				      f"Success on try {nr - retries_left + 1}: {result}")
				setattr(retry, attr_name,
				        getattr(retry, attr_name, 0) + nr - retries_left + 1)
				return result
			except Exception as e:
				print(f"{func.__name__:10s}: "
				      f"Failed on try  {nr - retries_left + 1}: {e}")
				retries_left -= 1
		setattr(retry, attr_name, getattr(retry, attr_name, 0) + nr)
		
		raise ValueError(f"Failed over {nr} tries.")
	
	return wrapper


@retry(nr=5)
def roll_high() -> int:
	"""retry roll high (>=5)"""
	
	result = randint(1, 6)
	if result < 5:
		raise ValueError(result)
	return result


try:
	roll_high()
except ValueError:
	pass


@retry()
def roll_low() -> int:
	"""retry roll low (<=2)"""
	
	result = randint(1, 6)
	if result > 2:
		raise ValueError(result)
	return result


try:
	roll_low()
except ValueError:
	pass

print(f"Total tries for retry: {getattr(retry, 'try_count', 0)}.\n")


def retry_2(nr: int = 3) -> Callable[[Any], Any]:
	"""One way of supporting arguments for decorator functions... This does
	not require a (optional) keyword argument, but does NOT allow for
	automatically using wrapped function as func argument when using:
	@new_retry
	def wrapped_func(): ...
	
	@new_retry()        # works, uses default value for nr.
	@new_retry(nr=5)    # works, uses specified value for nr.
	@new_retry(5)       # works, since now 5 is interpreted as nr arg.
	@new_retry          # does NOT work, decorated function is interpreted as
						# nr, resulting in 'new_retry.<locals>.decorator()
						# missing 1 # required positional argument: 'func''
	See also retry function above."""
	
	def decorator(func: Callable[[Any], Any]) -> Callable[[Any], Any]:
		"""This is the actual decorator function..."""
		
		print(f"Retry_2 decorator for {func.__name__:10s} with {nr} tries.")
		
		@wraps(func)
		def wrapper(*args: Any, **kwargs: Any) -> Any:
			"""The wrapper function around func."""
			
			# We use an attribute on the new_retry function to create state,
			# where we store the total nr of tries for all wrapped functions.
			attr_name = "new_try_count"
			
			retries_left = nr
			while retries_left > 0:
				try:
					result = func(*args, **kwargs)
					print(f"{func.__name__:10s}: "
					      f"Success on try {nr - retries_left + 1}: {result}")
					setattr(
						retry_2, attr_name,
						getattr(retry_2, attr_name, 0) + nr - retries_left + 1)
					return result
				except Exception as e:
					print(f"{func.__name__:10s}: "
					      f"Failed on try  {nr - retries_left + 1}: {e}")
					retries_left -= 1
			setattr(retry_2, attr_name, getattr(retry_2, attr_name, 0) + nr)
			raise ValueError(f"Failed over {nr} tries.")
		
		return wrapper
	
	return decorator


@retry_2(5)
def new_roll_high() -> int:
	"""return result >= 5"""
	result = randint(1, 6)
	if result < 5:
		raise ValueError(result)
	return result


try:
	new_roll_high()
except ValueError:
	pass


@retry_2()
def new_roll_low() -> int:
	"""return result < 3"""
	result = randint(1, 6)
	if result > 3:
		raise ValueError(result)
	return result


try:
	new_roll_low()
except ValueError:
	pass

print(f"Total tries for retry_2: {getattr(retry_2, 'new_try_count', 0)}.\n")
