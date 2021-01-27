from cs50 import get_float

while True:
    change = get_float("Change owed: ")
    if change > 0:
        break

money = int(round(change * 100))
coins = 0

for i in [25, 10, 5, 1]:
    coins += money // i
    money = money % i

print(coins)