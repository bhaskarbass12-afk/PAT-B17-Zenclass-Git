"""With import function"""

import math

input_num = float(input("enter the value:"))
round_off= math.ceil(input_num)
print(round_off)

"""without import function"""
input_num = float(input("Enter the value: "))
result = int(input_num) + 1
if input_num > int(input_num):
    print(result)
else:
    print("enter postive integer more than 0")
it will not work for negative scenerio

