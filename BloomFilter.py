"""A bloomfilter implementation. A bloomfilter can be used if you frequently
need to query a large set of data from external source (database) that cannot
be stored in memory (because of its size). Read items one by one, add them to
the filter. Now you can query for existence without (re)loading the items in
memory. Very memory-efficient, but has the risk of false positives. Before
processing a positive, check if it is false or not!"""

from hashlib import sha256, sha1, md5, sha384, sha512
from math import log, ceil
from random import choice
from string import ascii_lowercase


hash_functions = [sha256, sha1, md5, sha384, sha512]


class BloomFilter:

	"""The bloomfilter class supports adding to and querying the filter.
	Deleting is not an option since bits in filter_data may be set due to
	multiple items in the filter. Clearing a bit when deleting one item would
	wrongly also remove bit-sharing items."""
	
	def __init__(self, expected_nr_items: int, max_fpr: float) -> None:
		# self.size: int = size
		
		self.size = ceil(- (expected_nr_items * log(max_fpr) / (log(2) ** 2)))
		optimal_hashes = ceil(self.size / expected_nr_items * log(2))
		self.nhash: int = max(1, min(optimal_hashes, len(hash_functions)))
		num_bytes: int = (self.size + 7) // 8
		# Initialize a bytearry with all zeros
		self.filter_data = bytearray(([0] * num_bytes))

	def _hash(self, data: str, seed: int) -> int:
		
		hasher = hash_functions[seed]()
		hasher.update(data.encode())
		digest = int(hasher.hexdigest(), 16)
		return digest % self.size
	
	def add(self, item: str) -> None:
		"""Add item to filter."""
		
		for i in range(self.nhash):
			index = self._hash(item, seed=i)
			byte_index, bit_index = divmod(index, 8)
			mask = 1 << bit_index
			self.filter_data[byte_index] |= mask

	def query(self, item: str) -> bool:
		"""Return True if item PROBABLY in filter, False if CERTAINLY NOT in
		filter."""
		
		for i in range(self.nhash):
			index = self._hash(item, seed=i)
			byte_index, bit_index = divmod(index, 8)
			mask = 1 << bit_index
			if not (self.filter_data[byte_index] & mask):
				return False
		
		return True


class CountingBloomFilter(BloomFilter):
	"""The counting bloomfilter class supports adding to, querying and deleting
	from the filter. This comes with a cost of more memory, since we no longer
	set a bit, but use a counter (integer)."""
	
	def __init__(self, expected_nr_items: int, max_fpr: float) -> None:
		super().__init__(expected_nr_items, max_fpr)
		self.filter_data = bytearray(([0] * self.size))
	
	def add(self, item: str) -> None:
		"""Add item to filter."""
		
		for i in range(self.nhash):
			self.filter_data[self._hash(item, seed=i)] += 1
	
	def query(self, item: str) -> bool:
		"""Return True if item PROBABLY in filter, False if CERTAINLY NOT in
		filter."""
		
		for i in range(self.nhash):
			if self.filter_data[self._hash(item, seed=i)] == 0:
				return False
		
		return True

	def delete(self, item: str) -> None:
		"""Delete item from filter IF IT EXISTS. This is dangerous, since item
		may be a FALSE positive! Make sure the false positive ratio is low!"""
		
		indices_to_decrease = []
		
		for i in range(self.nhash):
			if (self.filter_data[index := self._hash(item, seed=i)]) <= 0:
				return
			indices_to_decrease.append(index)

		for index in indices_to_decrease:
			self.filter_data[index] -= 1
			
		
if __name__ == "__main__":
	
	# def print_filter(bloom_filter: BloomFilter) -> None:
	# 	"""Print the filter's filter_data content as integers"""
	# 	for i in range(len(bloom_filter.filter_data)):
	# 		print(f"0x{bloom_filter.filter_data[i]:02x}", end=',')
	#
	# 	print()

	def rnd_str(length: int) -> str:
		"""Return string of random lowercase ascii chars of specified length."""
		
		return ''.join(choice(ascii_lowercase) for _ in range(length))
	
	def _main() -> None:
		
		nr_strings = 1000
		chars_per_string = 10

		in_filter = [rnd_str(chars_per_string) for _ in range(nr_strings)]
		not_in_filter = [rnd_str(chars_per_string) for _ in range(nr_strings)]
		# Make sure no strings in not_in_filter are also in in_filter!
		intersect_items = set(in_filter).intersection(not_in_filter)
		for item in intersect_items:
			not_in_filter.remove(item)

		max_fpr = 0.07
		
		bloom_filter = BloomFilter(nr_strings, max_fpr)
		counting_bloom_filter = CountingBloomFilter(nr_strings, max_fpr)

		# add items to both filters
		for item in in_filter:
			bloom_filter.add(item)
			counting_bloom_filter.add(item)
			
		# check that all items are found when queried for
		for item in in_filter:
			assert bloom_filter.query(item)
			assert counting_bloom_filter.query(item)
			
		# items in not_in_filter should not be found. IF they're found anyway,
		# they constitute false positives.
		bloom_filter_false_positives = 0
		counting_bloom_filter_false_positives = 0
		
		for item in not_in_filter:
			possible_bf_fp = bloom_filter.query(item)
			possible_cbf_fp = counting_bloom_filter.query(item)
			if possible_bf_fp or possible_cbf_fp:
				if item not in in_filter:
					bloom_filter_false_positives += int(possible_bf_fp)
					counting_bloom_filter_false_positives += int(possible_cbf_fp)
	
		# report some statistics
		expected_false_positive = len(in_filter) * max_fpr
		ratio = bloom_filter_false_positives/expected_false_positive
		c_ratio = counting_bloom_filter_false_positives/expected_false_positive
		print(f"{bloom_filter.nhash=}, max_fpr={max_fpr/100:6.2%}\n"
		      f"ratio bf fp ({bloom_filter_false_positives}) / "
		      f"expected fp ({expected_false_positive:.0f}): "
		      f"{ratio:.0f}\n"
		      f"ratio cbf fp ({counting_bloom_filter_false_positives}) / "
		      f"expected fp ({expected_false_positive:.0f}): "
		      f"{c_ratio:.0f}")

		# Now delete from counting bloom filter and check deletion.
		false_positives_during_deletion = 0
		for i, item in enumerate(in_filter):
			sum_before = sum(counting_bloom_filter.filter_data)
			counting_bloom_filter.delete(item)
			# If after deletion the item is still found, it's a false positive
			if counting_bloom_filter.query(item):
				false_positives_during_deletion += 1
			sum_after = sum(counting_bloom_filter.filter_data)
			# The sum of all counts shoule decrease by filter.nhash for each
			# deleted item.
			assert sum_before - sum_after == counting_bloom_filter.nhash

			# Make sure all not yet deleted items are still there
			for remaining_item in in_filter[i + 1:]:
				assert counting_bloom_filter.query(remaining_item)
		
		# when all are deleted, all filter data should be zero
		assert all(i == 0 for i in counting_bloom_filter.filter_data)
		
		# report some more...
		print(f"{false_positives_during_deletion=}")
		
	_main()
