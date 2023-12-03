grid = []

while True:
	try:
		grid.append(input())
	except EOFError:
		break

print(f"size: {len(grid)} rows x {len(grid[0])} cols")
# print(f"grid={grid}")

def is_in_bounds(x, y):
	if 0 <= x and x < len(grid[0]) and 0 <= y and y < len(grid):
		return True
	return False

def is_part(num, y1, xmin, xmax):
	x = xmin-1
	y = y1-1
	while x < xmax + 1:
		if is_in_bounds(x, y):
			if not grid[y][x].isdigit() and grid[y][x] != '.':
				return True
		if is_in_bounds(x, y+1) and (x == xmin-1 or x == xmax):
			if not grid[y+1][x].isdigit() and grid[y+1][x] != '.':
				return True
		if is_in_bounds(x, y+2):
			if not grid[y+2][x].isdigit() and grid[y+2][x] != '.':
				return True
		x = x + 1
	return False

parts = []

for y in range(len(grid)):
	left = 0
	right = 0
	for x in range(len(grid[0]) + 1):
		# print(f"x={x},y={y},left={left},right={right}"), 
		if x == len(grid[0]) or not grid[y][x].isdigit():
			if right > left:
				num = int(grid[y][left:right])
				if is_part(num, y, left, right):
					parts.append(num)
			left = x + 1
			right = x + 1
		else:
			right = x + 1
# print(f"parts: {parts}")
print(f"parts sum={sum(parts)}")
		
