"""starred items in for loops"""
import itertools

if __name__ == "__main__":

	def main() -> None:
		"""Try combining all kinds of starred items."""
		
		r_1 = range(10)
		r_2 = range(50, 55)
		t_1 = (100, 200, 300)
		l_1 = ['a', 'b', 'c']
		
		items_1, items_2, items_3 = [], [], []
		# The following supplies FOUR starred_items
		for i in *r_1, *r_2, *t_1, *l_1:
			items_1.append(i)
		print(items_1, items_2, items_3)

		# The following supplies FOUR starred_items
		for i in (*r_1, *r_2, *t_1, *l_1):
			items_2.append(i)
		print(items_1, items_2, items_3)

		# The following supplies ONE starred_item, built by chaining FOUR items
		for i in itertools.chain(r_1, r_2, t_1, l_1):
			items_3.append(i)
		print(items_1, items_2, items_3)

		assert items_1 == items_2 == items_3
		print("All starred items processing ok.")
	main()
