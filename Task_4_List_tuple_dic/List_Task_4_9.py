List = [10, 20, 30, 9]
value = 59
n = len(List)
found=False
for i in range(n):
    for j in range(i + 1, n):
        for k in range (j + 1, n):
            if List[i] + List[j] + List[k] == value:
                print("triplet found:", List[i], List[j], List[k])
                found = True
                break
        if found:
            break
    if found:
        break
if not found:
        print("list is not matched with value when we create triplet")

