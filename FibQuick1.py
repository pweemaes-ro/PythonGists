"""A somewhat quick way to calculate the n-th fib number fib(n), with
fib(0) = 0, fib(1) = 1, and fib(n + 2) = fib(n + 1) + fib(n) for n in
{0, 1, 2, ...}."""

from __future__ import annotations

from collections.abc import Generator
from time import perf_counter_ns
from functools import lru_cache, reduce, wraps
from operator import mul, pow
from sys import set_int_max_str_digits
from typing import TypeAlias, TypeVar, Callable, ParamSpec, NamedTuple

matrix: TypeAlias = tuple[tuple[int, int], tuple[int, int]]

T = TypeVar("T")
P = ParamSpec("P")


def twos_complement(n: int) -> int:
	"""Return the int that is represented by the two's complement of n."""

	# To get the two's complement of (say) n = 108 = 0b1101100,
	# a) flip all bits to get 0b0010011
	# b) add 1 to get 0b0010100.

	# Many systems are two's complement systems and then the two's complement
	# of n is simply -n. Only use this function on systems that are not two's
	# complement systems. On two's complement systems this function will be
	# replaced by function neg_n (see below).
	
	return ~n + 1


def time_me(f: Callable[P, T]) -> Callable[P, T]:
	"""Report timing of call to f."""

	@wraps(f)
	def _timed_f(*args: P.args, **kwargs: P.kwargs) -> T:
		t_0 = perf_counter_ns()
		result = f(*args, **kwargs)
		t_1 = perf_counter_ns()
		print(f"{f.__qualname__}({args[1]}) took "
		      f"{(t_1 - t_0) * 10 ** -9:<03.2f} secs.")
		return result
	
	return _timed_f


class QuickFib:
	"""A simple class for quick calculations of fib(n)."""
	
	class FibMatrix:
		"""A simple 2x2 matrix class that supports * (__mul__) operator for
		multiplication and ** (__pow__) FOR EXPONENTS THAT ARE POWERS OF 2."""
		
		def __init__(self, _matrix: matrix):

			self.matrix = _matrix
		
		def __mul__(self, other: QuickFib.FibMatrix) -> QuickFib.FibMatrix:

			a = self.matrix[0][0]
			b = self.matrix[0][1]
			c = self.matrix[1][0]
			d = self.matrix[1][1]
			e = other.matrix[0][0]
			f = other.matrix[0][1]
			g = other.matrix[1][0]
			h = other.matrix[1][1]
			
			return QuickFib.FibMatrix(((a * e + b * g, a * f + b * h),
			                           (c * e + d * g, c * f + d * h)))
		
		def pow_cache_info(self) -> NamedTuple:
			"""Return cache info for the cache holding powers of self."""
			
			# Note: cache_info is a named tuple (not a string).
			return self.__pow__.cache_info()
		
		@lru_cache()
		def __pow__(self, power: int) -> QuickFib.FibMatrix:
			"""Return matrix ** power. Is rRecursive, but should be safe as
			long as no powers with more than 400 or so set bits are used..."""
			
			assert isinstance(power, int)
			assert power >= 1
			
			if power == 1:
				return self
			
			# power MUST itself be a power of 2, that is, power can be written
			# as power = 2 ** k for some integer k >= 1 (we've already ruled
			# out k = 0 <=> power = 2 ** k = 1, see above).
			assert len(list(QuickFib.get_exps(power))) == 1
			
			# It may seem smart to assign self ** power to a var to avoid
			# calculating twice, but the results of ** are cached, so there's
			# not much to gain... We use simple math rule:
			# m ** power = m ** (power / 2) * m ** (power / 2)
			m = self ** (power >> 1)
			return m * m
			
		def __repr__(self) -> str:
			return f"{self.__class__.__name__}({self.matrix})"
	
	M = FibMatrix(((1, 1), (1, 0)))
	
	def pow_cache_info(self) -> NamedTuple:
		"""Return cache info for the cache holding powers of M."""
		
		return self.M.pow_cache_info()
	
	@lru_cache(maxsize=None)
	def _fib(self, n: int) -> int:

		assert isinstance(n, int)
		assert n >= 0

		if n < 2:
			return n

		m_powers = (pow(self.M, exp) for exp in self.get_exps(n - 1))
		return reduce(mul, m_powers).matrix[0][0]  # type: ignore[no-any-return]

	@time_me
	def fib(self, n: int) -> int:
		"""Return the n-th fib nr. f(n), that is, the n-th number in sequence
		f(0), f(1), f(2), f(3), ... = 0, 1, 1, 2, 3, 5, 8, 13, etc."""

		return self._fib(n)

	def fib_cache_info(self) -> NamedTuple:
		"""Return cache info for the cache holding fib nrs."""
		
		# Note: cache_info is a named tuple (not a string).
		return self._fib.cache_info()
	
	@staticmethod
	def get_exps(n: int) -> Generator[int, None, None]:
		"""Returns list exps = [2 ** k_1, 2 ** k_2, 2 ** k_3, ..., 2 ** k_m]
		with k_1 > k_2 > k_3 > ... > k_m, such that n = sum(exps)."""
		
		# Example: since bin(236) = 0b11101100 <=>
		# 236 = 4 + 8 + 32 + 64 + 128 (all terms powers of 2), so
		# n_to_bin(236) = [4, 8, 32, 64, 128].
		
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
		# The result of n ^ t (bitwise XOR) sets the least significant set bit
		# of n to 0:
		# n     = 1101100 (108)
		# t     = 0000100 (  4)
		# n ^ t = 1101000 (104)
		#
		# As a result the loop is executed once for every set bit in n, that
		# is, a value 2 ** p is yielded for bit at position p if set in n.

		while n:
			# Do not use 'yield(t:=n & twos_complement(n))', since PyCharm
			# gives a false warning to remove the 'redundant' but in fact
			# MANDATORY braces!
			t = n & twos_complement(n)
			yield t
			n ^= t


def _main() -> None:
	
	set_int_max_str_digits(3000000)

	m = 1234567
	qf = QuickFib()

	print(f"{list(qf.get_exps(m))=}")
	print(f"fib({m}) has {len(str(qf.fib(m)))} digits.")
	print(f"{qf.pow_cache_info()=}")
	print(f"{qf.fib_cache_info()=}")


_main()
