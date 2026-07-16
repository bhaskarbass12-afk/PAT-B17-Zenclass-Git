# n = int(input())
# if n <= 1000:
#     for i in range(1,n+1):
#         if n % i == 0:
#             print(i, end=" ")
# else:
#     print("invalid value")

# n = int(input())
# factors = [i for i in range(1, n + 1) if n % i == 0]
# for f in factors:
#     print(f, end=' ')

n = int(input())
factors = [str(i) for i in range(1, n + 1) if n % i == 0]
print(factors)
print(" ".join(factors))
