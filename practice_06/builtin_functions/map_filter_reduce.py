from functools import reduce

nums = [1, 2, 3, 4, 5]

squared = list(map(lambda x: x**2, nums))
print("Squared:", squared)

even = list(filter(lambda x: x % 2 == 0, nums))
print("Even:", even)

sum_all = reduce(lambda x, y: x + y, nums)
print("Sum:", sum_all)