List = [1,2,5,10]
target = 10
count = 0

print(f"All ways to make Rs {target}:")

# Try all possible combinations
for rs10 in range(2):  # 0 or 1 (can't use more than 1)
    for rs5 in range(3):  # 0, 1, or 2 (can't use more than 2)
        for rs2 in range(6):  # 0 to 5 (can't use more than 5)
            for rs1 in range(11):  # 0 to 10 (can't use more than 10)
                # Check if this combination equals Rs 10
                if rs10 * 10 + rs5 * 5 + rs2 * 2 + rs1 * 1 == target:
                    count += 1
                    print(f"{count}. Rs10:{rs10}, Rs5:{rs5}, Rs2:{rs2}, Rs1:{rs1}")

print(f"Total ways: {count}")