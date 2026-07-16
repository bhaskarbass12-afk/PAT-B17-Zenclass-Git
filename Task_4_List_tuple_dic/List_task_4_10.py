List=[4,2,-3,1,6]
n = len(List)
found = False
sublist=[]

for i in range(n):
     total = 0
     for j in range(i, n):
         total += List[j]
         if total == 0:
             sublist = List[i:j+1]
             found = True
             break
     if found:
            break
if found:
    print("sublist with sum 0:", sublist)
else:
    print("No sublist with sum 0")