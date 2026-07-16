List = [10, 501, 22, 37, 100, 999, 87, 351]
for i in List:
    n = i
    seen = set()
    while n != 1 and n not in seen:
        seen.add(n)
        sum = 0
        for d in str(n):
            sum += int(d) ** 2
        n=sum
    if sum==1:
            print(i)
