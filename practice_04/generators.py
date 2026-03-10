#task number 1
def squares(N):
    for i in range(1,N+1):
        yield i**2

N=int(input())
for num in squares(N):
    print(num)


#task number 2
def even_nums(N):
    for i in range(0,N+1):
        if i%2==0:
            yield i
N=int(input())
print(",".join(str(num) for num in even_nums(N)))


#task number 3
def check(N):
    for i in range(0,N+1):
        if i%3==0 and i%4==0:
            yield i

N=int(input())
for num in check(N):
    print(num, end=" ")


#task number 4
def squares(a,b):
    for i in range(a,b+1):
        yield i**2
a,b=map(int, input().split())
for num in squares(a,b):
    print(num)


#task number 5
def reversion(N):
    for i in range(N,-1,-1):
        yield i
N=int(input())
for num in reversion(N):
    print(num)
