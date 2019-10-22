import numpy as np

height = 3
width = 7
room = np.empty((height, width))

positions = ((i, j) for i in range(height) for j in range(width))

for i, j in positions:
    room[i, j] = 1

pos = (2, 3)

cap = 5
dirt_amount = room[pos[0], pos[1]]
dirt_amount = max(dirt_amount - cap, 0)


bool(room[0,0])

room[0,0] = 0
bool(room[0,0])