""" Dice problem: Given an initial configuration of a dice, and a sequence of
rolls, what is the dice config after the roll?"""
from typing import TypeAlias

# We label each side according to initial configuration.
faces = ("U", "D", "L", "R", "F", "B")

# A roll to the left (ULDF) moves U to L, L to D, D to F and F to U, a roll to
# the right is reversed left.
LEFT_TRANSFORM = "ULDR"     # RIGHT is reverse, so RDLU
FRONT_TRANSFORM = "UFDB"    # BACK is reverse, so BDFU
roll_to_transformations = {'L': LEFT_TRANSFORM,
                           'R': LEFT_TRANSFORM[::-1],
                           'F': FRONT_TRANSFORM,
                           'B': FRONT_TRANSFORM[::-1]}


Face: TypeAlias = str
FaceValue: TypeAlias = str
Dice: TypeAlias = dict[Face, FaceValue]


def do_rolls(dice: Dice, rolls: str) -> Dice:
	"""Perform the specified roll(s) and return Dice after rolls."""
	
	for roll in rolls:
		transformation = roll_to_transformations[roll]
		new_dice = dict()
		for current_face, value in dice.items():
			if (current_face_index := transformation.find(current_face)) != -1:
				new_dice[transformation[(current_face_index + 1) % 4]] = value
			else:
				new_dice[current_face] = value
		dice = new_dice

	return dice
