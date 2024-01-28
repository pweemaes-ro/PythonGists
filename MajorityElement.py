"""Majority Vote and Frequent Items calculations.
- majority_vote_brute_force is very slow
- majority_vote_count_bm (bm stands for "Boyer-Moore) is faster, but..
- majority_vote_count() is the fastest algo to find the majority vote. It is
  basically a special version of frequent_items() for k=1.
- frequent_items uses Boyer-Moore like algo, but is slow
- frequent_items_count is 4 to 8 times faster.
With 80500 votes we have (times in seconds):
majority_vote_dict       : 0.10385560000577243
majority_vote_count      : 0.04342719999840483
majority_vote_count_bm   : 0.047338199998193886
frequent_items           : 0.2698223000043072
frequent_items_count     : 0.038736700000299606

Conclusion: Try to use Python batteries (they are implemented in C and usually
much faster than any Python loop construction)."""

from collections import defaultdict, Counter
from collections.abc import Callable
from random import randint, shuffle
from timeit import timeit
from typing import Any, TypeAlias

ResultPair: TypeAlias = tuple[Any, int]
ResultPairs: TypeAlias = tuple[ResultPair, ...]


def majority_vote_brute_force(votes: list[Any]) -> None | tuple[Any, int]:
	"""Return the vote that had the majority (> half) of votes, or None if no
	vote has such a majority. This version uses brute force and has time
	complexity O(n ** 2) and space complexity O(1)."""
	
	treshold = len(votes) // 2
	
	for vote in votes:
		count = 0
		for counted_vote in votes:
			if counted_vote == vote:
				count += 1
		if count > treshold:
			return vote, count
	
	return None


def majority_vote_dict(votes: list[Any]) -> ResultPair | None:
	"""Return the vote that had the majority (> half) of votes, or None if no
	vote has such a majority. This version uses a dictionary to keep track of
	the frequency counts, and has amortized time complexity O(n) - amortized,
	since the dict may end up being O(n ** 2) if hash collisions are frequent -
	and space complexity O(n)."""
	
	treshold = len(votes) // 2
	
	results: dict[int, Any] = defaultdict(int)
	
	for vote in votes:
		results[vote] += 1
		if results[vote] > treshold:
			return vote, results[vote]
	
	return None


def majority_vote_count(votes: list[Any]) -> ResultPair | None:
	"""Return the vote that had the majority (> half) of votes, or None if no
	vote has such a majority. This version uses collections.Counter to count
	the frequencies of all different votes and for retrieving the count for the
	most frequent vote. THIS VERSION IS SUBSTANTIALLY FASTER THAN THE OTHERS."""
	
	if len(votes) == 0:
		return None
	
	[(vote, count)] = Counter(votes).most_common(1)
	if count > len(votes) // 2:
		return vote, count
	
	return None


def majority_vote_count_bm(votes: list[Any]) -> ResultPair | None:
	"""Return the vote that had the majority (> half) of votes, or None if no
	vote has such a majority. This version uses Boyer-Moore algorithm."""
	
	if len(votes) == 0:
		return None
	
	candidate = votes[0]
	count = 0
	for vote in votes:
		if vote == candidate:
			count += 1
		elif count == 0:
			candidate = vote
			count = 1
		else:
			count -= 1
	
	if (nr_votes := votes.count(candidate)) > len(votes) // 2:
		return candidate, nr_votes
	
	return None


def frequent_items(votes: list[Any], k: int = 1) \
	-> ResultPair | ResultPairs | None:
	"""Return a tuple of at most k pairs (vote, count) that have more than
	len(votes) // (k + 1) votes, or None if no votes qualified. Special case:
	if k == 1, this returns the majority vote and its count as a tuple:
	(vote, count) or none if no votes qualified."""
	
	if len(votes) == 0:
		return None

	if k < 1:
		raise ValueError(f"Invalid k value: {k} (must be positive integer).")
	
	counts: dict[Any, int] = dict()
	
	for vote in votes:
		if vote in counts:
			counts[vote] += 1
		else:
			counts[vote] = 1
			if len(counts) > k:
				new_counts = dict()
				for candidate, count in counts.items():
					if count > 1:
						new_counts[candidate] = count - 1
				counts = new_counts

	counts_check = dict.fromkeys(counts, 0)
	for vote in votes:
		if vote in counts:
			counts_check[vote] += 1

	# We sort on nr of votes (using negation to sort descending)
	results = tuple(sorted(((vote, count)
	                       for (vote, count) in counts_check.items()
	                       if count > len(votes) // (k + 1)),
	                      key=lambda t: -t[1]))

	if k == 1:
		# for compatibility with majority_vote_... all_funcs
		# Revealed type is "tuple[Any, builtins.int]"
		return results[0] if results else None
	else:
		# Revealed type is "builtins.tuple[tuple[Any, builtins.int], ...]"
		return results


def frequent_items_count(votes: list[Any], k: int = 1) \
	-> ResultPair | ResultPairs | None:
	"""Return a tuple of at most k pairs (vote, count) that have more than
	len(votes) // (k + 1) votes, or None if no votes qualified. Special case:
	if k == 1, this returns the majority vote and its count as a tuple:
	(vote, count) or none if no votes qualified."""

	if len(votes) == 0:
		return None
	
	if k < 1:
		raise ValueError(f"Invalid k value: {k} (must be positive integer).")

	treshold = len(votes) // (k + 1)
	counter = Counter(votes)
	
	# We sort on nr of votes (using negation to sort descending)
	results = tuple((vote, count)
	                for vote, count in sorted(counter.most_common(k),
	                                          key=lambda vc_tpl: -vc_tpl[1])
	                if count > treshold)
	if k == 1:
		# for compatibility with majority_vote_... all_funcs
		# Revealed type is "tuple[Any, builtins.int]"
		return results[0] if results else None
	else:
		# Revealed type is "builtins.tuple[tuple[Any, builtins.int], ...]"
		return results


if __name__ == "__main__":

	inputs_and_results: \
		tuple[tuple[list[Any], ResultPair | ResultPairs | None], ...] = \
		(
			([1, 2, 2, 3, 3, 3, 4, 5, 6, 7, 7, 7, 7, 8, 8, 8, 8, 8, 9], None),
			([1, 2, 3, 3, 3, 4, 5, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7], (7, 9)),
			([1, 7, 2, 7, 3, 7, 3, 7, 3, 7, 4, 7, 5, 7, 7, 6, 7], (7, 9)),
			([(None, 1), (None, 2), (None, 2), 6, (None, 2)], ((None, 2), 3)),
			([], None),
			([1, 2, 3, 4, 5, 6], None),
			([2, 2, 2, 3, 1, 1, 1, 1], None),
		)
	
	all_funcs: (
		tuple)[Callable[[list[Any]], ResultPair | ResultPairs | None], ...] = (
		majority_vote_brute_force,
		majority_vote_dict,
		majority_vote_count,
		majority_vote_count_bm,
		frequent_items,
		frequent_items_count,
	)

	def _test_all(verbose: bool = False) -> None:
		"""Simple test function. Frequency algo's only test with k=1."""
		
		for _input, result in inputs_and_results:
			for f in all_funcs:
				assert (r := f(_input)) == result, \
					(f"{f.__qualname__}({_input}), "
					 f"{r} (expected: {result})")
				if verbose:
					print(f"{f.__qualname__}({_input}),\n\t {r}")
		print("All OK.")
	
	def timing() -> None:
		"""Prints the times to execute each function (with identical input)."""

		nr_votes = 8_500
		data = (list(randint(1, 100) for _ in range(nr_votes // 2)) +
		        ([0] * (1 + nr_votes // 2)))
		shuffle(data)
		print(f"{nr_votes=}, result={(0, 1 + nr_votes // 2)}")

		for func in all_funcs:
			if func.__qualname__ == "majority_vote_brute_force":    # too slow.
				continue
			print(f"{func.__qualname__:25s}: ", end="")
			print(timeit(stmt=f"{func.__qualname__}({data})",
			             number=1,
			             globals=globals()))

	_test_all(verbose=True)
	timing()
