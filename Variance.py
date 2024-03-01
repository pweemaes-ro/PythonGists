"""Several examples with explanation concerning covariance, contravariance and
invariance in Python"""
from copy import copy
from typing import (Generic, Callable, TypeAlias, TypeVar, NewType, Any,
	ParamSpec)
import logging


class Animal:
	"""Base class of Cat and Dog..."""
	
	...


class Dog(Animal):
	"""Base class of BullDog, BernseseMountainDog, GermanShepherd, Pug and
	Poodle...."""
	
	...


class BullDog(Dog):
	"""A specific dog..."""
	
	...


class BernseseMountainDog(Dog):
	"""A specific dog..."""
	
	...


class GermanShepherd(Dog):
	"""A specific dog..."""
	
	...


class Pug(Dog):
	"""A specific dog..."""
	
	...


class Poodle(Dog):
	"""A specific dog..."""
	
	def do_poodle_petting(self) -> None:
		"""This method on poodle may not be available on any other type of Dog,
		and therefor a function expecting a Dog object as param may not be
		replaced by a similar function expecting a Poodle."""
		
		print(f'{self.__class__.__name__} says: '
			  '"Ooh yeah! I love the way you stroke my... back."')


class Cat(Animal):
	"""A cat..."""

	...


# noinspection PyUnusedLocal
def poodle_creator(index: int) -> Poodle:
	"""Create and return a Poodle instance."""
	
	return Poodle()


def dog_creator(index: int) -> Dog:
	"""Create and return a Dog. Which kind of dog depends on index..."""
	
	if index < 7:
		return Pug()
	else:
		return BullDog()


# noinspection PyUnusedLocal
def cat_creator(index: int) -> Cat:
	"""Create and return a Cat."""
	
	return Cat()


def animal_creator(index: int) -> Animal:
	"""Create and return an Animal. Which kind of animal depends on index."""
	
	all_types = (Animal, Dog, BullDog, GermanShepherd, Pug, Poodle, Cat)
	return all_types[index % len(all_types)]()


T = TypeVar("T")

CreateFunction: TypeAlias = Callable[[int], T]
# type CreateFunction = Callable[[int], T]


def puppy_generator(nr_puppies: int, create_function: CreateFunction[Dog]) \
	-> list[Dog]:
	"""Generate nr_puppies (of any kind of dog) and return them in a list. The
	type of puppy is dependent on the return type of the creator_func."""
	
	puppies: list[Dog] = []
	for index in range(nr_puppies):
		puppies.append(create_function(index))
	return puppies


# noinspection PyUnusedLocal
def covariant_demo() -> None:
	"""The puppy_generator expects a creator_func of type PuppyCreator, which
	is a Callable expecting an int as parameter and returns type T. A Callable
	is covariant in its return type, so you can safely use a Callable with a
	more specific return type than Dog (say: Poodle), but not a callable with
	a less specific return type (say Animal).
	
	The poodle_creator returns a Poodle, which is a subtype of Dog, so
	passing poodle_creator where type Creator is expected, is safe. You could
	also say that it is safe to a assign the return value list[Poodle] to a
	var expecting a Dog, since every Poodle is a also a Dog, and every
	function on a Dog is also a function on a Poodle."""
	
	poodles: list[Dog] = puppy_generator(5, poodle_creator)
	
	# The dog_creator is a Callable returning a Dog, which is a subtype of Dog,
	# so the following is safe.

	dogs: list[Dog] = puppy_generator(5, dog_creator)
	
	# The animal_creator is a Callable returning an Animal, which is NOT a
	# subtype of Dog, so passing animal_creator where Creator is expected is
	# UNSAFE. You could also say that it should not be allowed to assign the
	# return value Animal to a var expecting a Dog, since an Animals may not be
	# a Dog, and not every function on a Dog is also a function on an Animal
	# (say: Dog.bark()).
	
	# animals: list[Dog] = puppy_generator(5, animal_creator)   # Error


# noinspection PyUnusedLocal
def pet_poodle(poodle: Poodle) -> None:
	"""Pet the poodle and make it very happy ;-)."""
	
	poodle.do_poodle_petting()


# noinspection PyUnusedLocal
def pet_dog(dog: Dog) -> None:
	"""Pet the dog and make it very happy ;-)."""
	
	...


# noinspection PyUnusedLocal
def pet_animal(animal: Animal) -> None:
	"""Pet the animal and make it very happy ;-)."""
	
	...


PetFunction: TypeAlias = Callable[[T], None]


def petting_zoo(pet_function: PetFunction[Dog]) -> None:
	"""Pet all kinds of dogs..."""
	
	# Suppose pet_poodle was allowed as pet_function. This function has a Poodle
	# object as its param. Now what could go wrong if we call that function on
	# a GermanShephard object... The GermanShephard object may not have the
	# function called in the pet_poodle function:
	pet_function(GermanShepherd())
	pet_function(BullDog())
	pet_function(BernseseMountainDog())
	pet_function(Dog())
	...


def contravariant_demo() -> None:
	"""The petting_zoo function expects param pet to be a PetFunction, which is
	a Callable expecting a variable of type Dog. We could then also safely pass
	any kind of subtype of Dog, say a GermanShepherd, to the pet function. Now
	suppose we were allowed to pass as pet function a Callable expecting a
	variable of a subtype of Dog, say Poodle. This pet function might call a
	Poodle method that's not available on GermanShephard -> runtime
	error! Or: Since Poodle is a subtype of Dog, every function on Dog is also
	a functon on Poodle, but NOT the other way around: a function on Poodle may
	not be a function on Dog. So if we pass a function expecting a Poodle, and
	that calls a function on Poodle, this function may not be a function on the
	passed object (Dog or any subtype of Dog other than Poodle).
	Passing a pet function that expects a (more generic) supertype of Dog
	(say Animal) as param is ok, since Dog is a subtype of Animal, so every
	function on an Animal is also a function on Dog."""
	
	# Alternative explanation: A function expecting a given type T as param
	# may call functions/methods on type T. Since every subtype S of T also
	# supports these functions/methods, it is safe to pass vars of subtype S to
	# the function, but not variables of supertype U, since functions on T may
	# not be available on variables of supertype U.
	
	# petting_zoo(pet_poodle)	   # Error
	petting_zoo(pet_dog)
	petting_zoo(pet_animal)


CloneFunction: TypeAlias = Callable[[T], T]


def clone_poodle(poodle: Poodle) -> Poodle:
	"""Return a copy of the poodle."""
	
	return copy(poodle)


def clone_dog(dog: Dog) -> Dog:
	"""Return a copy of the dog."""
	
	return copy(dog)


def clone_animal(animal: Animal) -> Animal:
	"""Return a copy of the animal."""
	
	return copy(animal)


def clone_my_doggo(clone_function: CloneFunction[Dog]) -> Dog:
	"""Return a copy of a newly created GermanShepherd."""
	
	return clone_function(GermanShepherd())


def invariant_demo() -> None:
	"""clone_my_doggo expects a CloneFunction[T] where T is Dog, that is a
	function with signature Callable[[Dog], Dog]. Since here Dog is both a
	parameter (which is always contravariant, not allowing subtypes of Dog) and
	a return type (which is always covariant, not allowing a supertype of Dog),
	only a function which expects a param of type Dog and returns a value of
	type Dog is allowed, that is, the clone_function is invariant in both the
	parameter type and the return type."""
	
	# Following fails for Mypy:
	# a) clone_my_doggo's parameter is typed as a Callable[[Dog], Dog], that
	# 	is, it returns a Dog, which cannot be assigned to a variable typed as
	# 	poodle, since Dog is not a subtype of Poodle, that is, a Dog is not
	# 	necessarilly a Poodle.
	# b) clone_my_doggo's parameter is typed as a Callable[[Dog], Dog], which
	# 	is invariant in both parameter and return type, so clone_poodle typed
	# 	as Callable[[Poodle], Poodle] is not safe.
	# poodle: Poodle = clone_my_doggo(clone_poodle)
	
	# noinspection PyUnusedLocal
	dog: Dog = clone_my_doggo(clone_dog)
	
	# a) clone_my_doggo's parameter is typed as a Callable[[Dog], Dog], which
	# 	is invariant in both parameter and return type, so clone_poodle typed
	# 	as Callable[[Poodle], Poodle] is not safe.
	# NOTE that it IS okay to assign a Dog to a variable typed Animal, since
	# Dog is a subtype of Animal, that is, a Dog is an Animal.
	# animal: Animal = clone_my_doggo(clone_animal)


covariant_demo()
contravariant_demo()
invariant_demo()

"""Conclusions:

1. Callable[[...], T] is covariant in type variable T:
- supplying a Callable[[...], T] is safe.
- supplying a Callable[[...], S] with S <: T is safe.
- supplying a Callable[[...], U] with T <: U is unsafe.

2. Callable[[T], ... is contravariant in type variable T:
- supplying a Callable[[T], ...] is safe.
- supplying a Callable[[U], ...] with T <: U is safe.
- supplying a Callable[[S], ...] with S <: T is unsafe.

3. Callable[[T], T] is invariant in type variable T.
- supplying a Callable[[T], T] is safe.
- supplying a Callable[[S], ...] with S <: T is unsafe.
- supplying a Callable[[U], ...] with T <: U is unsafe.
- supplying a Callable[[...], S] with S <: T is unsafe.
- supplying a Callable[[...], U] with T <: U is unsafe.

4. list[T] is invariant in type variable T, since lists are mutable and should
   only contain objects of a single type. If it was covariant in T, we could
   append an item of S <:T to a variable of type list[T].
   
5. Sequence[T] is covariant in type variable T, since Sequence is immutable, so
   adding items (of type T or other type) is impossible."""

C = TypeVar('C', covariant=True)
# C = TypeVar('C')


# class Box(Generic[T_co]):  # this type is declared covariant
class Box(Generic[C]):  # this type is declared covariant
	"""A generic class that overrules default (invariant) to covariant."""
	def __init__(self, content: C) -> None:
		self._content = content

	def get_content(self) -> C:
		"""Return content."""
		return self._content


# noinspection PyUnusedLocal
def look_into(box: Box[Animal]) -> None:
	"""Function taking box of Animal as param."""
	...


my_box = Box(Cat())
# Since Box is covariant in type T_co, it is allowed to pass subtype Box(Cat())
# as param to look_into (since Box(Cat) is subtype of Box(Animal), and Box is
# covariant in its type variable T_co.
look_into(my_box)  # OK, but mypy would complain here for an invariant type

"""NewType vs. alias:

- name = NewType(name, tp) is considered a subtype of tp by static type
  checkers. As a consequence, you cannot assign a tp value to name. To create a
  variable of type name, use name(value) where value is of type tp.

	UserID = NewType("UserID", int)
	
	my_userid = UserID(5)	   # Fine
	other_userid: UserID = 5	# should be flagged as error by typecheckers.
	
- Use TypeAlias to indicate that an assignment should be recognized as a proper
  type alias definition by type checkers.

	UserID = int
	my_userid = UserId(5)   # Fine
	my_userid = 5		   # Also fine (5 and UserID are both of type int)
	
"""
UserID = NewType("UserID", int)	 # Create type UserID as SUBTYPE of type int

UserIDToName: dict[UserID, str] = {UserID(1): "Paul"}


def get_username(user_id: UserID) -> str:
	"""get username"""
	return UserIDToName.get(user_id, "Not Found")


def get_userid(name: str) -> UserID:
	"""get user id"""
	for user_id, _name in UserIDToName.items():
		if _name == name:
			return user_id
	return UserID(-1)				   # Fine
	# return -1						   # Error


# user_id_1: UserID = 4				   # Error
some_int_1: int = UserID(1)			 # Fine
get_username(UserID(1))				 # Fine
# get_username(1)						 # Error
some_int_2: int = get_userid("Paul")    # Fine
user_id_2: UserID = get_userid("Paul")  # Fine

UserIDAlias: TypeAlias = int				   # type UserIDAlias is EQUIVALENT to type int
UserIDAliasToName: dict[UserIDAlias, str] = {UserIDAlias(1): "Paul"}


def _get_username(user_id: UserIDAlias) -> str:
	return UserIDAliasToName.get(user_id, "Not Found")


def _get_userid(name: str) -> UserIDAlias:
	for user_id, _name in UserIDAliasToName.items():
		if _name == name:
			return user_id
	return -1


_user_id: UserIDAlias = 4	   # Error
_some_int: int = 1   # Fine
print(_get_username(_some_int))
some_int = _get_userid("Paul")
print(some_int)


z: tuple[Any, ...] = ("foo", "bar")
print(z)
# These reassignments are OK: plain `tuple` is equivalent to `tuple[Any, ...]`
z = (1, 2, 3)
print(z)
z = ()
print(z)
	

P = ParamSpec('P')


# def add_logging[T, **P](f: Callable[P, T]) -> Callable[P, T]:
def add_logging(f: Callable[P, T]) -> Callable[P, T]:
	"""A type-safe decorator to add logging to a function."""
	def inner(*args: P.args, **kwargs: P.kwargs) -> T:
		"""The replacement func"""
		logging.info(f'{f.__name__} was called')
		return f(*args, **kwargs)
	return inner


@add_logging
def add_two(x: float, y: float) -> float:
	"""Add two numbers together."""
	return x + y
