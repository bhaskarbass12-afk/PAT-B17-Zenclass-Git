import math

N, M = map(int, input().split())
product = N*M
if product < 0:
    print("No")
else:
    sqrt = int(math.sqrt(product))
    if sqrt * sqrt == product:
        print("Yes")
    else:
        print("No")
