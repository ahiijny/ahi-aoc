from math import prod

grid = []
adjs = {}

while True:
	try:
		grid.append(input())
	except EOFError:
		break

print(f"size: {len(grid)} rows x {len(grid[0])} cols")
# print(f"grid={grid}")

for y in range(len(grid)):
	for x in range(len(grid[0])):
		adjs[(x,y)] = []

def is_in_bounds(x, y):
	if 0 <= x and x < len(grid[0]) and 0 <= y and y < len(grid):
		return True
	return False

def calc_adj_part(num, y1, xmin, xmax):
	x = xmin-1
	y = y1-1
	while x < xmax + 1:
		if is_in_bounds(x, y):
			if not grid[y][x].isdigit() and grid[y][x] != '.':
				adjs[(x,y)].append(num)
		if is_in_bounds(x, y+1) and (x == xmin-1 or x == xmax):
			if not grid[y+1][x].isdigit() and grid[y+1][x] != '.':
				adjs[(x,y+1)].append(num)
		if is_in_bounds(x, y+2):
			if not grid[y+2][x].isdigit() and grid[y+2][x] != '.':
				adjs[(x,y+2)].append(num)
		x = x + 1

parts = []

for y in range(len(grid)):
	left = 0
	right = 0
	for x in range(len(grid[0]) + 1):
		# print(f"x={x},y={y},left={left},right={right}"), 
		if x == len(grid[0]) or not grid[y][x].isdigit():
			if right > left:
				num = int(grid[y][left:right])
				calc_adj_part(num, y, left, right)
			left = x + 1
			right = x + 1
		else:
			right = x + 1

gear_ratios = []
			
for y in range(len(grid)):
	for x in range(len(grid[0])):
		if grid[y][x] == '*':
			if len(adjs[(x,y)]) == 2:
				gear_ratios.append(prod(adjs[(x,y)]))
			
print(f"gear ratios sum={sum(gear_ratios)}")
		
