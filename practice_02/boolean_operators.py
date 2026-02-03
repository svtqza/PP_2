#!
sum1 = 100 + 50      # 150 (100 + 50)
sum2 = sum1 + 250    # 400 (150 + 250)
sum3 = sum2 + sum2   # 800 (400 + 400)

#2
numbers = [1, 2, 3, 4, 5]

if (count := len(numbers)) > 3:
    print(f"List has {count} elements")

#3
x = 5
y = 3

print(x == y)
print(x != y)
print(x > y)
print(x < y)
print(x >= y)
print(x <= y)

#4
x = ["apple", "banana"]
y = ["apple", "banana"]
z = x

print(x is z)
print(x is y)
print(x == y)

#5
fruits = ["apple", "banana", "cherry"]

print("pineapple" not in fruits)
