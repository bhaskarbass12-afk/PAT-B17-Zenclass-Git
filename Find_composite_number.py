N = int(input())
if N <= 1:
    print("no")
else:
    is_composite = False
    for i in range(2,N):
        if N % i == 0:
            is_composite = True
            break
    if is_composite:
        print("yes")
    else:
        print("no")