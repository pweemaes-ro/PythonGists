"""Test fib implementations."""

from sys import set_int_max_str_digits

import pytest

from Fibonacci.fib_closed_form import QuickFibClosed as QF_Closed
from Fibonacci.quick_fib_pp import QuickFibPP as QF_Pure_Python
from Fibonacci.quick_fib_np_cached import QuickFibNPCached as QF_Numpy_cached
from Fibonacci.quick_fib_np_uncached import (
	QuickFibNPUncached as QF_Numpy_uncached)

set_int_max_str_digits(3000000)


@pytest.fixture()
def qf_python() -> QF_Pure_Python:
	"""Fixture returns a pure python class implementation."""
	
	return QF_Pure_Python()


@pytest.fixture()
def qf_numpy_cached() -> QF_Numpy_cached:
	"""Fixture returns a class implementation using numpy for matrix
	multiplication (but not for matrix power calculations)."""
	
	return QF_Numpy_cached()


@pytest.fixture()
def qf_numpy_uncached() -> QF_Numpy_uncached:
	"""Fixture returns a class implementation using numpy for matrix
	multiplication (but not for matrix power calculations)."""
	
	return QF_Numpy_uncached()


@pytest.fixture()
def qf_closed() -> QF_Closed:
	"""Fixture returns a class implementation using Phi Rational ring."""
	
	return QF_Closed()


fib_data = \
	[
		[0, "0", "0", 1],
		[1, "1", "1", 1],
		[2, "1", "1", 1],
		[3, "2", "2", 1],
		[12, "144", "144", 3],
		[123, "22698", "75682", 26],
		[1234, "34774", "48487", 258],
		[12345, "40080", "27970", 2580],
		[123456, "26830", "51392", 25801],
		[1234567, "78446", "95853", 258009],
		# [12345678, "57945", "00264", 2580094]
	]


@pytest.mark.parametrize(
	"n, first_five, last_five, length", fib_data
)
def test_fib_python(qf_python: QF_Pure_Python,
                    n: int,
                    first_five: str,
                    last_five: str,
                    length: int) -> None:
	fib_n = qf_python.fib(n)
	s = str(fib_n)
	assert first_five == s[:5]
	assert last_five == s[-5:]
	assert length == len(s)


@pytest.mark.parametrize(
	"n, first_five, last_five, length", fib_data
)
def test_fib_numpy_cached(qf_numpy_cached: QF_Numpy_cached,
                          n: int,
                          first_five: str,
                          last_five: str,
                          length: int) -> None:
	fib_n = qf_numpy_cached.fib(n)
	s = str(fib_n)
	assert first_five == s[:5]
	assert last_five == s[-5:]
	assert length == len(s)


@pytest.mark.parametrize(
	"n, first_five, last_five, length", fib_data
)
def test_fib_numpy_uncached(qf_numpy_uncached: QF_Numpy_uncached,
                            n: int,
                            first_five: str,
                            last_five: str,
                            length: int) -> None:
	fib_n = qf_numpy_uncached.fib(n)
	s = str(fib_n)
	assert first_five == s[:5]
	assert last_five == s[-5:]
	assert length == len(s)


@pytest.mark.parametrize(
	"n, first_five, last_five, length", fib_data
)
def test_fib_closed_form(qf_closed: QF_Closed,
                         n: int,
                         first_five: str,
                         last_five: str,
                         length: int) -> None:
	fib_n = qf_closed.fib(n)
	s = str(fib_n)
	assert first_five == s[:5]
	assert last_five == s[-5:]
	assert length == len(s)
