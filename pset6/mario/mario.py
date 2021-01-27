from cs50 import get_int

n = -1 # initialize the variable so that the condition below is met

while True:
    n = get_int("please type a number betweeen 1 and 8:")
    if n > 0 and n <= 8:
        break

for i in range(1, n+1):
    print(' ' * (n-i) + '#' * i)


