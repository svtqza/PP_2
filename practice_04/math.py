#task number 1
import math

degree = float(input("Input degree: "))
radian = degree * (math.pi / 180)
print("Radian:", round(radian, 6))


#task number 2
height = float(input("Height: "))
base1 = float(input("Base, first value: "))
base2 = float(input("Base, second value: "))
area = (base1 + base2) * height / 2

print("Area:", area)


#task number 3
import math

n = int(input("Input number of sides: "))
s = float(input("Input the length of a side: "))
area = (n * s**2) / (4 * math.tan(math.pi / n))
print("Area:", area)


#task number 4
base = float(input("Length of base: "))
height = float(input("Height of parallelogram: "))
area = base * height
print("Area:", area)

