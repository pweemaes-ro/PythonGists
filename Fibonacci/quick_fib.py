"""Functionality used by multiple fib implementations and a base class for Fib
implementations."""

from __future__ import annotations

from abc import abstractmethod, ABC
from collections.abc import Callable, Generator
from functools import wraps, lru_cache
from time import perf_counter_ns
from typing import TypeVar, ParamSpec, TypeAlias

import numpy as np

T = TypeVar("T")
P = ParamSpec("P")
matrix: TypeAlias = tuple[tuple[int, int], tuple[int, int]]


def twos_complement(n: int) -> int:
	"""Return the int that is represented by the two's complement of n."""
	
	# To get the two's complement of (say) n = 108 = 1101100,
	# a) flip all bits to get 0010011
	# b) add 1 to get 0010100.
	
	# Many systems are two's complement systems and then the two's complement
	# of n is simply -n (negative n). This function also works on systems that
	# don't represent negative integers in two's complement!

	assert isinstance(n, int)
	assert n >= 0
	
	return ~n + 1


def get_powers_of_two(n: int) -> Generator[int, None, None]:
	"""Yield in increasing order all powers of 2 that sum up to n."""
	
	# Example: 236 = 4 + 8 + 32 + 64 + 128 (all terms powers of 2), so
	# get_powers_of_two(n) yields (in this order) 4, 8, 32, 64, 128.
	
	assert isinstance(n, int)
	assert n >= 0
	
	# The result of 'bitwise AND'ing a number n with its two's complement
	# is all 0 bits except for the least significant set bit in n, so if
	# n = 108 then:
	# n                             = 1101100 (108)
	# two's complement of n         = 0010100 ( 20)
	# t = n & two's complement of n = 0000100 (  4)
	# which is 2 ** p with p = 2 the zero-based bitposition of the least
	# significant set bit in n.
	#
	# n^t (bitwise XOR) sets the least significant 1 bit of n to 0:
	# n   = 1101100 (108)
	# t   = 0000100 (  4)
	# n^t = 1101000 (104)
	#
	# So the loop is executed once for every set bit in n.
	
	while n:
		# noinspection PyRedundantParentheses
		yield (t := n & twos_complement(n))
		n ^= t


def mat_mul(first: matrix, second: matrix) -> matrix:
	"""Return matrix product first * second. Both matrices must be 2 x 2."""
	
	assert len(first) == len(second) == 2
	assert len(first[0]) == len(second[0]) == 2
	assert len(first[1]) == len(second[1]) == 2
	
	a = first[0][0]
	b = first[0][1]
	c = first[1][0]
	d = first[1][1]
	e = second[0][0]
	f = second[0][1]
	g = second[1][0]
	h = second[1][1]
	
	return ((a * e + b * g, a * f + b * h),
	        (c * e + d * g, c * f + d * h))


__M = ((1, 1), (1, 0))


@lru_cache(maxsize=400)
def power_of_m_np(power: int) -> matrix:
	"""Return matrix ** power. Is recursive, but should be safe as long
	as no powers > 2 ** 1000 or so are used (a number of 302 digits)..."""
	
	assert isinstance(power, int)
	assert power >= 1
	
	if power == 1:
		return __M
	
	# Make sure power is itself a power of 2.
	assert len(list(get_powers_of_two(power))) == 1
	
	h = np.array(power_of_m_np(power >> 1), dtype=object)
	r = np.matmul(h, h)
	return r[0], r[1]

	
@lru_cache(maxsize=400)  # That should suffice ;-)
def power_of_m(power: int) -> matrix:
	"""Return matrix ** power. Is recursive, but should be safe as long
	as no powers > 2 ** 1000 or so are used (a number of 302 digits)..."""
	
	assert isinstance(power, int)
	assert power >= 1
	
	if power == 1:
		return __M
	
	# Make sure power is itself a power of 2.
	assert len(list(get_powers_of_two(power))) == 1
	
	h = power_of_m(power >> 1)  # >> 1 = integer divide by 2, note: recursion!
	return mat_mul(h, h)


def time_fib(f: Callable[P, T]) -> Callable[P, T]:
	"""Report timing of call to f to stdout."""
	
	@wraps(f)
	def _timed_f(*args: P.args, **kwargs: P.kwargs) -> T:
		t_0 = perf_counter_ns()
		result = f(*args, **kwargs)
		t_1 = perf_counter_ns()
		print(f"{f.__qualname__}({args}) took "
		      f"{(t_1 - t_0) * 10 ** -9:<03.2f} secs.")
		return result
	
	return _timed_f


class QuickFib(ABC):
	"""The base class. Cannot be instantiated!"""
	
	def __init__(self) -> None:
		self.__fib_timed = False
		self._untimed_fib_func = self.fib
		self._timed_fib_func = time_fib(getattr(self, "fib"))

	def set_fib_timing(self, value: bool) -> None:
		"""Turn printing duration of fib(n) on or off."""

		if self.__fib_timed is not value:
			if value:   # must change to timed
				setattr(self, "fib", getattr(self, "_timed_fib_func"))
			else:       # must revert to untimed
				setattr(self, "fib", getattr(self, "_untimed_fib_func"))

			self.__fib_timed = value

	@abstractmethod
	@lru_cache(maxsize=None)
	def cached_fib(self, n: int) -> int:
		"""Cached version of fib(n). Must be implemented by derived classes."""

		...

	def fib(self, n: int) -> int:
		"""Return the n-th fib nr."""

		assert isinstance(n, int)
		assert n >= 0

		return self.cached_fib(n)
