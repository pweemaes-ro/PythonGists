"""Pretty fast way to calculate Fib(n)."""

# The basic ideas:
# a) Let M = [[1, 1], [1, 0]], then [[F(n+1)], [f(n)]] = (M ** n) * [[1], [0]].
# b) For all n >= 0: n = k_1 +  k_2 + ... + k_m with all k_i unique powers of 2.
# c) With n = sum(k_i) we have M ** n = prod(M ** k_i).
# c) With k_i = 2 ** x with x > 1 we have k_i / 2 a positive integer and
#    M ** k_1 = M ** (k_i / 2) * M ** (k_i / 2).
from __future__ import annotations

import timeit
from functools import reduce, lru_cache
from sys import set_int_max_str_digits
from typing import NamedTuple

from Fibonacci.fib_common import (time_me, get_powers_of_two, mat_mul, mat_pow,
	pow_cache_info)


class QuickFib:
	"""A simple class for quick calculations of fib(n)."""

	def __init__(self) -> None:
		self.m = ((1, 1), (1, 0))
		self.__fib_timed = False
		self._untimed_fib = self.fib

	def set_fib_timing(self, value: bool) -> None:
		"""Turn timing reporting on or off."""

		if self.__fib_timed is not value:
			if value:   # must change to timed
				setattr(self, "fib", time_me(getattr(self, "fib")))
			else:       # must revert to untimed
				setattr(self, "fib", getattr(self, "_untimed_fib"))

			self.__fib_timed = value

	@lru_cache(maxsize=None)
	def _fib(self, n: int) -> int:

		assert isinstance(n, int)
		assert n >= 0

		if n <= 2:
			return 1 if n == 2 else n

		# We use f(n) = f(n-2) + f(n-1) and if M ** (n-2) = [[a, b], [b, c]]
		# then [[f(n-2)], [f(n-1)]] = [[a], [b]] = sum(M ** (n-2)[0]) = f(n).
		return sum(reduce(mat_mul,
		                  (mat_pow(exp)
		                   for exp in get_powers_of_two(n - 2)))[0])

	def fib(self, n: int) -> int:
		"""Return the n-th fib nr."""

		return self._fib(n)

	def fib_cache_info(self) -> NamedTuple:
		"""Return cache info for the cache holding fib nrs."""

		return self._fib.cache_info()

	def clear_fib_cache(self) -> None:
		"""Clear all caches..."""
	
		self._fib.cache_clear()
	
	
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
	
	qb = QuickFib()
	
	# qb.set_fib_timing(True)
	print(timeit.timeit("_timeit(qb)", number=10, globals=globals()))
	print(f"{pow_cache_info()=}")
	print(f"{qb.fib_cache_info()=}")

	# qb.set_fib_timing(False)
	# print(timeit.timeit("_timeit(qb)", number=10, globals=globals()))
	# print(f"{pow_cache_info()=}")
	# print(f"{qb.fib_cache_info()=}")
