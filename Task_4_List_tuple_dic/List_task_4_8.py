ratings = [3.5, 3.8, 4.1, 4.2, 4.5, 4.7, 4.8, 4.9]

minimum = ratings[0]

for List in ratings:
    if List < minimum:
        minimum = ratings

print("Minimum rating:", minimum)
