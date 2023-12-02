from collections import deque
from functools import reduce

grid = []

while True:
	try:
		row = [int(x) for x in input()]
		grid.append(row)
	except EOFError:
		break
		
print(f"{len(grid)} x {len(grid[0])}")

L = len(grid)
H = len(grid[0])

vis = [[[0 for c in range(L)] for r in range(H)] for x in range(4)]

deltas = [
	[0, 1], # right
	[1, 0], # down
	[0, -1], # left
	[-1, 0] # up
]

print(f"vis:{len(vis)}x{len(vis[0])}x{len(vis[0][0])}")

for r in range(H):
	for c in range(L):
		for i, delta in enumerate(deltas):
			# print(f"r={r},c={c},i={i},delta={delta}")
			dr = delta[0]
			dc = delta[1]
			plat = grid[r][c]
			for x in range(1, max(H, L)+1):
				r2 = r + x * dr
				c2 = c + x * dc
				if r2 < 0 or r2 >= H or c2 < 0 or c2 >= L:
					x -= 1
					break
				if grid[r2][c2] >= plat:
					break
			vis[i][r][c] = x
				
		
def print_grid(grid):
	for r in grid:
		for c in r:
			print('1' if c == True else '0' if c == False else c, end='')
		print('\n', end='')

#print_grid(grid)
print()

#print(f"right:")
#print_grid(vis[0])
#print(f"down:")
#print_grid(vis[1])
#print(f"left:")
#print_grid(vis[2])
#print(f"up:")
#print_grid(vis[3])

best = -1

for r in range(H):
	for c in range(L):
		score = 1
		for i in range(4):
			score *= vis[i][r][c]
		if score > best:
			best = score
			print(f"best@[{r}][{c}]: {score}")



