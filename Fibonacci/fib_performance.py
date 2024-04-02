"""Run and report relative performance of all implementations."""
from sys import set_int_max_str_digits
from timeit import timeit

from Fibonacci.fib_closed_form import QuickFibClosed
from Fibonacci.quick_fib_np_cached import QuickFibNPCached
from Fibonacci.quick_fib_np_uncached import QuickFibNPUncached
from Fibonacci.quick_fib_pp import QuickFibPP

_test_data = \
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


def _timeit(quickfib: QuickFibNPCached,
            test_data: list[tuple[int, str, str, int]]) -> None:
	"""Run and report results of performance tests on all implementations."""
	
	test_data.reverse()
	
	for n, first, last, nr_digits in test_data:
		fib_n = quickfib.fib(n)
		fib_n_str = str(fib_n)
		assert fib_n_str[:5] == first
		assert fib_n_str[-5:] == last
		assert len(fib_n_str) == nr_digits


set_int_max_str_digits(3000000)

stmt = '_timeit(qb, _test_data)'
for qb in (QuickFibPP(),
           QuickFibNPUncached(),
           QuickFibNPCached(),
           QuickFibClosed()):
	print(f"{qb.__class__.__qualname__:20s}",
	      f"{timeit(stmt, number=10, globals=globals()):06.4f}")
