"""Numpy implementation of a pretty fast way to calculate Fib(n). This version
uses np.matmul for both calculating powers of m and product of powers of m, and
therefore uses caching of powers of m."""
from timeit import timeit
from functools import lru_cache, reduce
from sys import set_int_max_str_digits

from Fibonacci.quick_fib import QuickFib, get_powers_of_two, power_of_m_np
import numpy as np


class QuickFibNPCached(QuickFib):
	"""A simple class for quick calculations of fib(n)."""

	@lru_cache(maxsize=None)
	def cached_fib(self, n: int) -> int:
		"""Fast fib(n) calculation using NumPy."""
		
		assert isinstance(n, int)
		
		if n <= 2:
			return 1 if n == 2 else n
		
		return sum(reduce(np.matmul,
		                  (power_of_m_np(exponent)
		                   for exponent in get_powers_of_two(n - 2)))[0])


if __name__ == "__main__":
	def _clear_all_caches(quickfib: QuickFibNPCached) -> None:
		quickfib.cached_fib.cache_clear()
		power_of_m_np.cache_clear()


	def _timeit(quickfib: QuickFibNPCached) -> None:
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
	
		test_data.reverse()

		for n, first, last, nr_digits in test_data:
			fib_n = quickfib.fib(n)
			fib_n_str = str(fib_n)
			# print(fib_n_str)
			assert fib_n_str[:5] == first
			assert fib_n_str[-5:] == last
			assert len(fib_n_str) == nr_digits
	
	
	set_int_max_str_digits(3000000)
	
	qb = QuickFibNPCached()
	qb.set_fib_timing(False)
	print(timeit("_timeit(qb)", number=10, globals=globals()))
	print(f"{qb.cached_fib.cache_info()=}")
	print(f"{power_of_m_np.cache_info()=}")
	
	# qb.set_fib_timing(False)
	# print(timeit("_timeit(qb)", number=10, globals=globals()))
	# print(f"{qb.fib_cache_info()=}")
	# print(f"{power_of_m_np.cache_info()=}")
