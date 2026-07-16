# K_Moves, O_moves = map(int, input().split())
# Difference = O_moves - K_Moves
# print(Difference)

import sys

for line in sys.stdin:
    line = line.strip()
    if line:
        a, b = map(int, line.split())
        print(b - a)