x = input("enter the value:")
y = ''
for i in range(len(x)-1,-1,-1):
    print(x[i])
    y = y+x[i]
if y == x:
    print(f" {x} is palindrome")
else:
    print(f" {x} is not palindrome")