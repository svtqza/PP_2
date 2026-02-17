#1
x = lambda a : a + 10
print(x(5))

#2
def myfunc(n):
  return lambda a : a * n

mydoubler = myfunc(2)

print(mydoubler(11))

#3
def myfunc(n):
  return lambda a : a * n

mydoubler = myfunc(2)
mytripler = myfunc(3)

print(mydoubler(11))
print(mytripler(11))

#4
def myfunc(n):
  return lambda a : a * n

mytripler = myfunc(3)

print(mytripler(11))