# len = int(input())
# Breath = int(input())
# area = Breath * len
# print(area)

len, breath = map(float, input().split())
area = len * breath
result = int(area*100000)/100000
print(f"{result:.5f}")