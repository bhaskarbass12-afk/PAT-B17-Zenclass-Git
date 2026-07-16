N = int(input())
if N <= 100000000000:
    product = 1
    digits = str(N)
    for i in digits:
        product = product*int(i)
    print(product)
# #
# n = input()
# product = 1
# for d in n:
#     product *= int(d)
# print(product)



# def product_of_digits(n):
#     n = abs(n)  # Handle negative numbers
#     product = 1
#     while n > 0:
#         digit = n % 10
#         print(digit)
#         product = product*digit
#         n //= 10
#         print(n)
#     return product
#
# # Read input
# n = int(input())
# print(product_of_digits(n))