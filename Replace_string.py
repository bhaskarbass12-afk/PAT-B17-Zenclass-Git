# S = input()
# length = len(S)
# print(S[:2]) #start:Stop
# print(S[-2:]) #start:stop
# print(S[2:])

S = input()
length = len(S)
mid = length//2
if length%2 == 0:
    print(S[:mid-1]+ '**' + S[mid+1:])
if length%2 != 0:
    print(S[:mid]+ '*' + S[mid+1:])
