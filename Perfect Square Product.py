import math

N, M = map(int, input().split())
product = N*M
if product < 0:
    print("no")
else:
    square = int(math.sqrt(product))
    if square*square == product:
        print("yes")
    else:
        print("no")