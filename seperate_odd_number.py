n = int(input())
if n<=100000:
    digits = str(n)
    odd_digits = [i for i in digits if int(i) % 2 != 0]
    if odd_digits:
        print(" ".join(odd_digits))
    else:
        print(-1)
else:
    print("invalid number")