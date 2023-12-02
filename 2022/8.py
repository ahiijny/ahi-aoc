from collections import deque

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

visible = [[False for c in range(L)] for r in range(H)]

for r in range(H):
	highest = -1
	for c in range(L):
		if grid[r][c] > highest:
			visible[r][c] = True
		highest = max(highest, grid[r][c])
	
	highest = -1
	for c in range(L-1, -1, -1):
		if grid[r][c] > highest:
			visible[r][c] = True
		highest = max(highest, grid[r][c])
	
for c in range(L):
	highest = -1
	for r in range(H):
		if grid[r][c] > highest:
			visible[r][c] = True
		highest = max(highest, grid[r][c])
		
	highest = -1
	for r in range(H-1, -1, -1):
		if grid[r][c] > highest:
			visible[r][c] = True
		highest = max(highest, grid[r][c])
	
def print_grid(grid):
	for r in grid:
		for c in r:
			print('1' if c == True else '0' if c == False else c, end='')
		print('\n', end='')

#print_grid(grid)
#print()
#print_grid(visible)
print(f"visible: {sum([r.count(True) for r in visible])}")

	
