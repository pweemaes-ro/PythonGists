"""A somewhat quick way to calculate the n-th fib number fib(n), with
fib(0) = 0, fib(1) = 1, and fib(n + 2) = fib(n + 1) + fib(n) for n in
{0, 1, 2, ...}."""

# todo: Move twos_complement to other module
# todo: Move time_me to other module
from __future__ import annotations

import timeit
from functools import lru_cache, reduce
from sys import set_int_max_str_digits
from typing import NamedTuple

from Fibonacci.fib_common import (time_me, mat_pow, get_powers_of_two, mat_mul,
	pow_cache_info)

import numpy as np


class QuickFib:
	"""A simple class for quick calculations of fib(n)."""

	def __init__(self, cache_powers: bool = False):
		self.__m = np.array([[1, 1], [1, 0]], dtype=object)
		self.__cache_powers = cache_powers
		self.__fib_timed = False
		self.__untimed_fib = self.fib
	
	def set_fib_timing(self, value: bool) -> None:
		"""Turn timing reporting on or off."""
		
		if self.__fib_timed is not value:
			if value:  # must change to timed
				setattr(self, "fib", time_me(getattr(self, "fib")))
			else:  # must revert to untimed
				setattr(self, "fib", getattr(self, "_untimed_fib"))
			
			self.__fib_timed = value
	
	def clear_fib_cache(self) -> None:
		"""Clear fib cache..."""

		self._fib.cache_clear()
		
	@lru_cache(maxsize=None)
	def _fib(self, n: int) -> int:

		assert isinstance(n, int)
		assert n >= 0

		if n < 2:
			return n

		if n == 2:
			return 1

		if self.__cache_powers:
			return sum(reduce(mat_mul,
			           (mat_pow(exp)
			            for exp in get_powers_of_two(n - 2)))[0])
		else:
			return sum(np.linalg.matrix_power(self.__m, n - 2)[0])

	def fib(self, n: int) -> int:
		"""Return the n-th fib nr."""

		return self._fib(n)

	def fib_cache_info(self) -> NamedTuple:
		"""Return cache info for the cache holding fib nrs."""
		
		return self._fib.cache_info()


if __name__ == "__main__":
	def _clear_all_caches(quickfib: QuickFib) -> None:
		quickfib.clear_fib_cache()
		mat_pow.cache_clear()
	
	
	def _timeit(quickfib: QuickFib) -> None:
		# print(f"{pow_cache_info()=}")
		# print(f"{qb.fib_cache_info()=}")
		
		_clear_all_caches(quickfib)
		
		# print(f"{pow_cache_info()=}")
		# print(f"{qb.fib_cache_info()=}")
		
		test_data = \
			[
				(0, "0", "0", 1),
				(1, "1", "1", 1),
				(2, "1", "1", 1),
				(3, "2", "2", 1),
				(12, "144", "144", 3),
				(123, "22698", "75682", 26),
				(1234, "34774", "48487", 258),
				(12345, "40080", "27970", 2580),
				(123456, "26830", "51392", 25801),
				(1234567, "78446", "95853", 258009),
				# (12345678, "57945", "00264", 2580094)
			]
		
		for n, first, last, nr_digits in test_data:
			fib_n = quickfib.fib(n)
			fib_n_str = str(fib_n)
			assert fib_n_str[:5] == first
			assert fib_n_str[-5:] == last
			assert len(fib_n_str) == nr_digits
	
	
	set_int_max_str_digits(3000000)
	
	qb = QuickFib(True)
	# qb.set_fib_timing(True)
	print(timeit.timeit("_timeit(qb)", number=10, globals=globals()))
	print(f"{pow_cache_info()=}")
	print(f"{qb.fib_cache_info()=}")
	
	qb = QuickFib()
	# qb.set_fib_timing(False)
	print(timeit.timeit("_timeit(qb)", number=10, globals=globals()))
	print(f"{pow_cache_info()=}")
	print(f"{qb.fib_cache_info()=}")
