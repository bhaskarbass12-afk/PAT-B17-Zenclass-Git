List_1 = ['10', '20', '30', '40', '50']
List_2 = ['10', '11', '12', '15', '20']
List_3 = ['10', '30', '45', '60', '75']

duplicates=[]

for item in List_1:
    if item in List_2 and item in List_3:
        duplicates.append(item)
print(duplicates)