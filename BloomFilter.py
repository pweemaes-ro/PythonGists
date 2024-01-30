"""A bloomfilter implementation."""
from hashlib import sha256, sha1, md5, sha384, sha512
from math import log, ceil
from random import choice
from string import ascii_lowercase


hash_functions = [sha256, sha1, md5, sha384, sha512]


class BloomFilter:

	"""The bloomfilter class supports adding to and querying the filter."""
	
	def __init__(self, expected_nr_items: int, max_fpr: float) -> None:
		# self.size: int = size
		
		self.size = ceil(- (expected_nr_items * log(max_fpr) / (log(2) ** 2)))
		optimal_hashes = ceil(self.size / expected_nr_items * log(2))
		self.nhash: int = max(1, min(optimal_hashes, len(hash_functions)))
		num_bytes: int = (self.size + 7) // 8
		# Initialize a bytearry with all zeros
		self.bit_vector = bytearray(([0] * num_bytes))

	def _hash(self, data: str, seed: int) -> int:
		
		hasher = hash_functions[seed % len(hash_functions)]()
		hasher.update(data.encode())
		digest = int(hasher.hexdigest(), 16)
		return digest % self.size
	
	def add(self, item: str) -> None:
		"""Add item to filter."""
		
		for i in range(self.nhash):
			index = self._hash(item, seed=i)
			byte_index, bit_index = divmod(index, 8)
			mask = 1 << bit_index
			self.bit_vector[byte_index] |= mask

	def query(self, item: str) -> bool:
		"""Return True if item PROBABLY in filter, False if CERTAINLY NOT in
		filter."""
		
		for i in range(self.nhash):
			index = self._hash(item, seed=i)
			byte_index, bit_index = divmod(index, 8)
			mask = 1 << bit_index
			if not (self.bit_vector[byte_index] & mask):
				return False
		
		return True


class CountingBloomFilter:
	"""The counting bloomfilter class supports adding to, querying and deleting
	from the filter."""
	
	def __init__(self, expected_nr_items: int, max_fpr: float) -> None:
		self.size = ceil(- (expected_nr_items * log(max_fpr) / (log(2) ** 2)))
		optimal_hashes = ceil(self.size / expected_nr_items * log(2))
		self.nhash: int = max(1, min(optimal_hashes, len(hash_functions)))
		self.count_vector = bytearray(([0] * self.size))
	
	def _hash(self, data: str, seed: int) -> int:
		hasher = hash_functions[seed % len(hash_functions)]()
		hasher.update(data.encode())
		digest = int(hasher.hexdigest(), 16)
		return digest % self.size
	
	def add(self, item: str) -> None:
		"""Add item to filter."""
		
		for i in range(self.nhash):
			self.count_vector[self._hash(item, seed=i)] += 1
	
	def query(self, item: str) -> bool:
		"""Return True if item PROBABLY in filter, False if CERTAINLY NOT in
		filter."""
		
		for i in range(self.nhash):
			if self.count_vector[self._hash(item, seed=i)] == 0:
				return False
		
		return True

	def delete(self, item: str) -> None:
		"""Delete item from filter IF IT EXISTS. This is dangerous, since item
		may be a FALSE positive! Make sure the false positive ratio is low!"""
		
		indices_to_decrease = []
		
		for i in range(self.nhash):
			if (self.count_vector[index := self._hash(item, seed=i)]) <= 0:
				return
			indices_to_decrease.append(index)

		for index in indices_to_decrease:
			self.count_vector[index] -= 1
			
		
if __name__ == "__main__":
	
	def print_filter(bloom_filter: BloomFilter) -> None:
		"""Print the filter's bitvector content as integers"""
		for i in range(len(bloom_filter.bit_vector)):
			print(f"0x{bloom_filter.bit_vector[i]:02x}", end=',')
		
		print()

	def rnd_str(length: int) -> str:
		"""Return string of random lowercase ascii chars of specified length."""
		
		return ''.join(choice(ascii_lowercase) for _ in range(length))
	
	def _main() -> None:
		expected_nr_items = 1000
		items = list(rnd_str(10) for _ in range(expected_nr_items))
		probably_not_items = list(rnd_str(10) for _ in range(1000))
		max_fpr = 0.001
		
		bloom_filter = BloomFilter(expected_nr_items, max_fpr)
		counting_bloom_filter = CountingBloomFilter(expected_nr_items, max_fpr)

		for item in items:
			bloom_filter.add(item)
			counting_bloom_filter.add(item)
			
		for item in items:
			assert bloom_filter.query(item)
			assert counting_bloom_filter.query(item)
		
		bloom_filter_false_positives = 0
		counting_bloom_filter_false_positives = 0
		
		for unlikely_item in probably_not_items:
			possible_bf_fp = bloom_filter.query(unlikely_item)
			possible_cbf_fp = counting_bloom_filter.query(unlikely_item)
			if possible_bf_fp or possible_cbf_fp:
				if unlikely_item not in items:
					bloom_filter_false_positives += int(possible_bf_fp)
					counting_bloom_filter_false_positives += int(possible_cbf_fp)
	
		expected_false_positive = len(items) * max_fpr
		ratio = bloom_filter_false_positives/expected_false_positive
		c_ratio = counting_bloom_filter_false_positives/expected_false_positive
		print(f"{bloom_filter.nhash=}, "
		      f"ratio bf fp ({bloom_filter_false_positives}) / "
		      f"expected fp ({expected_false_positive:.0f}): "
		      f"{ratio:.0f}"
		      f"ratio cbf fp ({counting_bloom_filter_false_positives}) / "
		      f"expected fp ({expected_false_positive:.0f}): "
		      f"{c_ratio:.0f}")

		false_positives_during_deletion = 0
		for i, item in enumerate(items):
			sum_before = sum(counting_bloom_filter.count_vector)
			counting_bloom_filter.delete(item)
			if counting_bloom_filter.query(item):
				false_positives_during_deletion += 1
			sum_after = sum(counting_bloom_filter.count_vector)
			assert sum_before - sum_after == counting_bloom_filter.nhash

			for remaining_item in items[i+1:]:
				assert counting_bloom_filter.query(remaining_item)
		
		assert sum(counting_bloom_filter.count_vector) == 0
		print(f"{false_positives_during_deletion=}")
		
	_main()
