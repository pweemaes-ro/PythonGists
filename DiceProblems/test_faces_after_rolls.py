"""Obvious..."""
import pytest

from faces_after_rolls import faces, do_rolls

dice = {face: face for face in faces}


@pytest.mark.parametrize(
	# ("L", {"B": "B", "U": "R", "F": "F", "D":"L", "L":"U",
	#        "R":"D"})
	# means that after a Left roll ("L")
	# - the "B" face is the "B" face from before the roll
	# - the "U" face is the "R" face from before the roll.
	# - etc.
	["roll", "result"],
	[("L", {"B": "B", "F": "F", "U": "R", "D": "L", "L": "U", "R": "D"}),
	 ("R", {"B": "B", "F": "F", "U": "L", "D": "R", "L": "D", "R": "U"}),
	 ("F", {"L": "L", "R": "R", "B": "D", "U": "B", "F": "U", "D": "F"}),
	 ("B", {"L": "L", "R": "R", "B": "U", "U": "F", "F": "D", "D": "B"})]
)
def test_single_rolls(roll: str, result: dict[str, str]) -> None:
	"""Test all single rolls."""
	
	new_dice = do_rolls(dice, roll)

	for key in new_dice.keys():
		assert result[key] == new_dice[key]


@pytest.mark.parametrize(
	"rolls",
	["RL", "LR", "FB", "BF",
	 "RRLL", "LLRR", "FFBB", "BBFF",
	 "RRRR", "LLLL", "FFFF", "BBBB"],
)
def test_neutralizing_rolls(rolls: str) -> None:
	"""Test pairs and quadruple rolls that have no effect. It may seem
	pointless to verify this, since if each individual single roll is correct,
	then combined rolls will also be correct. However, this way the loop inside
	do_rolls function that deals with each individual roll in a combined roll
	like "LLRR" is also tested."""

	new_dice = do_rolls(dice, rolls)
	assert new_dice == dice
