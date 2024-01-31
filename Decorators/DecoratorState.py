"""Two ways of giving a decorator function state:
1. Using an attribute on the decorator function.
2. Using a decorator class instead of a decorator function.\
We will use a simple decorator (without any arguments other than the function
it should decorate), the technique applies to more complex variants in a
similar way."""
from collections.abc import Callable
from functools import wraps, update_wrapper
from typing import TypeVar, ParamSpec, Any, TypeAlias
from mypy_extensions import NamedArg

T = TypeVar('T')
P = ParamSpec('P')
G: TypeAlias = Callable[[int, NamedArg(int, 'exponent')], int]


def decorator(func: Callable[P, T]) -> Callable[P, T]:
	"""The decorator function with state in an attribute. The function creates
	and maintains a state attribute, which is a dict of whatever k, v pair the
	decorator wants to keep. In this case, it holds the nr of calls to func,
	which can be retrieved using:
	
	getattr(decorator, "state", {}).get('nr_calls', 0)."""

	@wraps(func)
	def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
		"""The function wrapping func."""
		
		print(f"func: Preprocessing here... ({args=}, {kwargs=})")
		result = func(*args, **kwargs)

		# modify state
		nr_calls = (state := getattr(decorator, "state", {})).get('nr_calls', 0)
		print(f"func: BEFORE: {nr_calls=}")

		print(f"func: modifying nr_calls: adding 1 to {nr_calls=}.")
		state['nr_calls'] = nr_calls + 1
		setattr(decorator, "state", state)

		nr_calls = getattr(decorator, "state", {}).get('nr_calls', 0)
		print(f"func: AFTER : {nr_calls=}")

		print(f"func: Postprocessing ({result=})")
		return result
	
	return wrapper


@decorator
def decorated_function(base: int, *, exponent: int) -> int:
	"""Just an example of a function using a decorator. Return base raised to
	the exponent."""
	
	# int() is required since ** has type Any, which causes Mypy to complain:
	# 'error: Returning Any from function declared to return "int".'
	return int(base ** exponent)


n = 5
for _ in range(n):
	# noinspection PyArgumentList
	decorated_function(2, exponent=3)

assert getattr(decorator, "state", {}).get('nr_calls', 0) == n


# 2. Using a decorator class

class Decorator:
	"""A simple decorator class without arguments (other than the decorated
	function). It has state *per decorated function*. For an example of state per
	decorator see DecoratorWithArgs class."""

	def __init__(self, func: Callable[P, T]):
		update_wrapper(self, func)
		self.func = func
		self.state: dict[str, Any] = {}
		
	def __call__(self, *args: P.args, **kwargs: P.kwargs) -> Any:
		
		print(f"class: Preprocessing here... ({args=}, {kwargs=}.")
		result = self.func(*args, **kwargs)

		# modify state
		nr_calls = self.get_state('nr_calls', 0)
		print(f"class: BEFORE: {nr_calls=}")
		print(f"class: modifying state: adding 1 to {nr_calls=}.")
		self.set_state('nr_calls', nr_calls + 1)
		print(f"class: AFTER : {self.get_state('nr_calls')=}")

		print(f"class: Postprocessing ({result=})")
		return result
	
	def get_state(self, name: str, default: Any = None) -> Any:
		"""Get value of name key in state dict, or default if not found."""
		
		return self.state.get(name, default)
	
	def set_state(self, name: str, value: Any) -> None:
		"""Set value for name key in state dict."""
		
		self.state[name] = value


@Decorator
def class_decorated_1(base: int, *, exponent: int) -> int:
	"""Example function decorated by Decorator class."""
	
	return int(base ** exponent)


@Decorator
def class_decorated_2(base: int, *, exponent: int) -> int:
	"""Example function decorated by Decorator class."""
	
	return int(base ** exponent)


n = 7
for _ in range(n):
	class_decorated_1(2, exponent=3)
	class_decorated_2(2, exponent=3)

assert (class_decorated_1.get_state('nr_calls') ==
        class_decorated_2.get_state('nr_calls') == n)


class DecoratorWithArgs:
	"""A decorator class which expects an argument - so parenthesis needed when
	using this decorator. It also supports decorator state in 'calls' (not per
	decorated function, but over all functions decorated with this class!"""
	
	state: dict[str, Any] = {}

	def __init__(self, init_nr_calls: int = 0) -> None:
		print(f"__init__({init_nr_calls=})")
		self.func: G | None = None

		cls = self.__class__
		calls = cls.get_class_state('nr_calls', 0)
		cls.set_class_state('nr_calls', calls + init_nr_calls)

	def __call__(self, func: G) -> G:
		
		@wraps(func)
		def wrapper(base: int, exponent: int) -> int:
			"""The wrapper function."""

			print(f"class: Preprocessing here... ({base=}, {exponent=})")

			assert self.func
			result = self.func(base, exponent=exponent)

			# modify state
			cls = self.__class__
			nr_calls = cls.get_class_state('nr_calls', 0)
			print(f"class: BEFORE: {nr_calls=}")
			print(f"class: modifying state: adding 1 to {nr_calls}.")
			cls.set_class_state('nr_calls', nr_calls + 1)
			print(f"class: AFTER : {cls.get_class_state('nr_calls')=}")

			print(f"class: Postprocessing ({result=})")
			return result

		return wrapper
	
	@classmethod
	def get_class_state(cls, name: str, default: Any = None) -> Any:
		"""Get value of name key in state dict, or default if not found."""

		return cls.state.get(name, default)

	@classmethod
	def set_class_state(cls, name: str, value: Any) -> None:
		"""Set value for name key in state dict."""

		cls.state[name] = value
	

@DecoratorWithArgs(5)
def class_decorated_3(base: int, *, exponent: int) -> int:
	"""A simple function to illustrate DecoratorWithArgs class decorator."""
	return int(base ** exponent)


# class_decorated_3 = DecoratorWithArgs(5)(class_decorated_3)


# @DecoratorWithArgs(5)
# def class_decorated_4(base: int, *, exponent: int) -> int:
# 	"""A simple function to illustrate DecoratorWithArgs class decorator."""
# 	return int(base ** exponent)
#
#
# class_decorated_4 = DecoratorWithArgs(5)(class_decorated_4)

# n = 5

# for _ in range(n):
# 	class_decorated_3(2, exponent=3)
# 	class_decorated_4(2, exponent=3)
# assert DecoratorWithArgs.get_class_state('nr_calls') == 2 * (n + 5)
