"""Example of a microservice implementation using coroutines (basically, a
coroutine is a specific type of generator)."""
from collections.abc import Generator
from typing import Any


# Suppose we have a generator function my_gen():
def my_gen() -> Generator[int, Any, None]:
	x = 0
	y = 0
	while True:
		print(f"Before y = yield(x), {x=}, {y=}, about to yield {x=}")
		y = yield(x)
		print(f"After  y = yield(x), {x=}, {y=}, assigned {y=}")
		if y is not None:
			x = 5 * y
			print(f"After x = 5 * y, {x=}, {y=}, calculated {x=}")
		else:
			print(f"After x = 5 * y, {x=}, {y=}, so could not calculate {x=}")

g = my_gen()
print("Executing: z = next(g)")
z = next(g)
# above line causes execution of my_gen() up to line: y = yield(x), which
# yields (returns) the current value of x (0) (which is assigned to z), but
# does NOT assign to y.
print(f"{z = }")

# print("Executing: z = g.send(None)")
# z = g.send(None)
# above line causes execution of my_gen() up to line: y = yield(x), which
# yields (returns) the current value of x (0) (which is assigned to z), but
# does NOT assign to y.
# print(f"{z = }")

print("Executing: z = g.send(2)")
z = g.send(2)
# above line causes continued execution of my_gen, starting with assigning the
# send value to y, then calculating x = 5 * y = 10, then starting new iteration
# of the while loop, up to line: y = yield(x), which yields (returns) the
# current value of x (10) (which is assigned to z), but does NOT assign to y.
print(f"{z = }")

print("Executing: z = next(g)")
z = next(g)
# above line causes continued execution of my_gen() up to line: y = yield(x),
# which yields (returns) the current value of x (0) (which is assigned to z),
# but does NOT assign to y.
print(f"{z = }")

print("Executing: z = g.send(None)")
z = g.send(None)
# above line causes continued execution of my_gen, starting with assigning the
# send value to y, then calculating x = 5 * y = 10, then starting new iteration
# of the while loop, up to line: y = yield(x), which yields (returns) the
# current value of x (10) (which is assigned to z), but does NOT assign to y.
print(f"{z = }")


# Let g = my_gen(), so g is a generator object. Assume we have primed the
# generator function (using next(g) or g.send(None)), then we can send data to
# g and request data from g. Suppose the local variable x in my_gen has value 10.
# a) z = g.send(23):
#    - g yields current value of x (10), so z = x = 10,
#    - g assigns the send value (23) to y, so y = 23.

# b) z = next(g):
#    - g yields current value of x (10), so z = x = 10,
#    - g since no value was sent, g assigns None to x.
# 	 So z = next(g) is equivalent to z = g.send(None)