N=int(input())
if N<=1000:
    digits = str(N)
    print(int(digits[::-1]))
else:
    print("invalid input")