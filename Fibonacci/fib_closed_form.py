"""A closed form for fib(n) using the ring Q(Phi)."""

from __future__ import annotations

from sys import set_int_max_str_digits
from functools import lru_cache, reduce
from operator import mul
from fractions import Fraction
from time import perf_counter_ns

from Fibonacci.quick_fib import get_powers_of_two, power_of_m
from Fibonacci.quick_fib_pp import QuickFibPP


# Math notes:
# fib(n) = (1 / sqrt(5)) * (phi ** n - psi ** n)
# with
# a) phi = (1 + sqrt(5)) / 2 => sqrt(5) = -1 + 2 * phi = PhiRational(-1, 2).
# b) phi = PhiRational(0, 1).
# c) psi = (1 - sqrt(5)) / 2 = (1 - (-1 + 2 * phi)) / 2 = PhiRational(1, -1).
# d) phi ** 2 = ((1 + sqrt(5)) / 2) ** 2 = 1 + (1 + sqrt(5)) / 2 = 1 + phi, so
#    phi ** 2 = 1 + phi = PhiRational(1, 1).
# e) ADDITION in PhiRational:
#    PhiRational(a, b) + PhiRational(c, d) =
#    (a + b * phi) + (c + d * phi) =
#    (a + c) + (b + d) * phi =
#    PhiRational(a + c, b + d).
# f) MULTIPLICATION in PhiRational:
#    PhiRational(a, b) * PhiRational(c, d) =
#    (a + b * phi) * (c + d * phi) =
#    ac + (ad * phi) + (bc * phi) + (bd * (phi ** 2)) =
#    ac + (ad * phi) + (bc * phi) + (bd * (1 + phi)) =
#    ac + (ad * phi) + (bc * phi) + bd + (bd * phi) =
#    ac + bd + (ad + bc + bd) * phi =
#    PhiRational(ac + bd, ad + bc + bd).


class PhiRational:
	"""PhiRational class, supports only what's needed for calculating fib(n)."""

	# coordindates for phi and psi
	phi = (0, 1)
	psi = (1, -1)
	
	PHI = 1.61803398875

	def __init__(self, a: Fraction | int, b: Fraction | int) -> None:
		
		self.a = Fraction(a)
		self.b = Fraction(b)

	def norm(self) -> Fraction:
		"""(Needed for __reciprocal)"""

		return Fraction(self.a ** 2 + self.a * self.b - self.b ** 2)

	def reciprocal(self) -> PhiRational:
		"""(Needed for __truediv__)"""

		return PhiRational((self.a + self.b) / self.norm(), -self.b / self.norm())

	def __int__(self) -> int:
		
		if self.b == 0:
			return int(self.a)
		else:
			return int(self.a + self.b * PhiRational.PHI)

	def __sub__(self, other: PhiRational) -> PhiRational:
		
		return PhiRational(self.a - other.a, self.b - other.b)
		
	def __mul__(self, other: PhiRational) -> PhiRational:

		a, b = self.a, self.b
		c, d = other.a, other.b
		
		return PhiRational(a * c + b * d, a * d + b * c + b * d)

	def __truediv__(self, other: PhiRational) -> PhiRational:

		return self * other.reciprocal()

	def __eq__(self, other: object) -> bool:
		assert isinstance(other, PhiRational)
		
		return self.a == other.a and self.b == other.b

	@staticmethod
	@lru_cache(maxsize=400)
	def phi_pow(n: int) -> PhiRational:
		"""Cached version of power of phi calculation."""

		if n == 1:
			return PhiRational(*PhiRational.phi)
		
		h = PhiRational.phi_pow(n >> 1)
		return h * h

	@staticmethod
	@lru_cache(maxsize=400)
	def psi_pow(n: int) -> PhiRational:
		"""Cached version of power of psi calculation."""
		
		# assert len(list(get_powers_of_two(n))) == 1
		
		if n == 1:
			return PhiRational(*PhiRational.psi)
	
		h = PhiRational.psi_pow(n >> 1)
		return h * h

	def __pow__(self, n: int) -> PhiRational:

		if self == PhiRational(*PhiRational.phi):
			return self.phi_pow(n)
		
		if self == PhiRational(*PhiRational.psi):
			return self.psi_pow(n)
		
		raise ValueError("__pow__ only supported for base phi and base psi!")
	
	def __repr__(self) -> str:
		return f'({self.a} + {self.b}φ)'


phi = PhiRational(0, 1)
psi = PhiRational(1, -1)
sqrt_5 = PhiRational(-1, 2)


@lru_cache
def fib_closed(n: int) -> int:
	"""Return the n-th fib nr."""
	
	assert isinstance(n, int)
	assert n >= 0
	if n < 2:
		return n
	
	powers = list(get_powers_of_two(n))

	powers_of_phi = list(phi ** power for power in powers)
	powers_of_psi = list(psi ** power for power in powers)
	
	nth_power_of_phi = reduce(mul, powers_of_phi)
	nth_power_of_psi = reduce(mul, powers_of_psi)
	
	return int((nth_power_of_phi - nth_power_of_psi) / sqrt_5)


if __name__ == "__main__":
	def _main() -> None:
		quickfib = QuickFibPP()
		set_int_max_str_digits(3000000)
		
		n = 45678
		for i in range(n-5, n+1):
			t_0 = perf_counter_ns()
			qf = str(quickfib.fib(i))
			t_1 = perf_counter_ns()
			qc = str(fib_closed(i))
			t_2 = perf_counter_ns()
			print(t_1 - t_0, qf[:5], qf[-5:])
			print(t_2 - t_1, qc[:5], qf[-5:])
			assert qf == qc
	
		print(power_of_m.cache_info())
		print(PhiRational.phi_pow.cache_info())
		print(PhiRational.psi_pow.cache_info())

	_main()
	