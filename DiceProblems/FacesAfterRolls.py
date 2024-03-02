""" Dice problem: Given an initial configuration of a dice, and a sequence of
rolls, what symbol is up after all rolls?"""

# We label each side according to initial configuration.
UP = 'U'
DOWN = 'D'
LEFT = 'L'
RIGHT = 'R'
FRONT = 'F'
BACK = 'B'

# A roll to the left (ULDF) moves U to L, L to D, D to F and F to U, a roll to
# the right is reversed left.
LEFT_TRANSFORM = "ULDF"
FRONT_TRANSFORM = "UFDB"
roll_to_transformations = {'L': LEFT_TRANSFORM,
                           'R': LEFT_TRANSFORM[::-1],
                           'F': FRONT_TRANSFORM,
                           'B': FRONT_TRANSFORM[::-1]}


def get_value(dice: dict[str, str], face_to_find: str) -> str:
	"""Return value on the specified face_to_find or None if face invalid."""
	
	for value, face in dice.items():
		if face == face_to_find:
			return value
	else:
		return ""


def do_rolls(dice: dict[str, str], rolls: str) -> dict[str, str]:
	"""Perform the specified rolls"""

	for roll in rolls:
		transformation: str = roll_to_transformations[roll]
		new_dice: dict[str, str] = dict()
		for value, current_face in dice.items():
			if (current_face_index := transformation.find(current_face)) != -1:
				new_dice[value] = transformation[(current_face_index + 1) % 4]
		dice = new_dice
	
	return dice


if __name__ == "__main__":
	def _main() -> None:
		dice = {'A': BACK,
		        'B': RIGHT,
		        'C': FRONT,
		        'D': UP,
		        'E': LEFT,
		        'F': DOWN}
	
		rolls = "LLFFRR"
		print(f"Before rolling {rolls}:")
		print(f"Letter on up side of the dice: "
		      f"{get_value(dice, UP)}")
		dice = do_rolls(dice, rolls)
		print(f"After rolling {rolls}:")
		print(f"Letter on up side of the dice: "
		      f"{get_value(dice, UP)}")

	_main()
