""" Dice problem: Given an initial configuration of a dice, and a sequence of
rolls, what is the dice config after the roll?"""

# We label each side according to initial configuration.
faces = ("U", "D", "L", "R", "F", "B")

# A roll to the left (ULDF) moves U to L, L to D, D to F and F to U, a roll to
# the right is reversed left.
LEFT_TRANSFORM = "ULDR"     # RIGHT: RDLU
FRONT_TRANSFORM = "UFDB"    # BACK: BDFU
roll_to_transformations = {'L': LEFT_TRANSFORM,
                           'R': LEFT_TRANSFORM[::-1],
                           'F': FRONT_TRANSFORM,
                           'B': FRONT_TRANSFORM[::-1]}


def get_value(dice: dict[str, str], face_to_find: str) -> str:
	"""Return value on the specified face_to_find or None if face invalid."""
	
	return dice[face_to_find]


def print_dice(dice: dict[str, str]) -> None:
	"""Print all faces and their labels."""
	
	for k, v in dice.items():
		print(f"{k}: {v}")


def do_rolls(dice: dict[str, str], rolls: str) -> dict[str, str]:
	"""Perform the specified rolls"""
	
	for roll in rolls:
		transformation: str = roll_to_transformations[roll]
		new_dice: dict[str, str] = dict()
		for current_face, value in dice.items():
			if (current_face_index := transformation.find(current_face)) != -1:
				new_dice[transformation[(current_face_index + 1) % 4]] = value
			else:
				new_dice[current_face] = value
		dice = new_dice

	return dice


if __name__ == "__main__":
	def _main() -> None:
		dice = {face: face for face in faces}
		rolls = "LLFFRR"

		print(f"Before rolling {rolls}:")
		print_dice(dice)

		dice = do_rolls(dice, rolls)

		print(f"After rolling {rolls}:")
		print_dice(dice)

	_main()
