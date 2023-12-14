vertical_mirrors = []
horizontal_mirrors = []

def in_bounds(grid, x, y):
	return 0 <= x and x < len(grid[0]) and 0 <= y and y < len(grid)
		
		
def process(grid):
	# find vertical flip
	
	for mirror_y in range(1, len(grid)):
		# print(f" testing y={mirror_y}")
		valid = True
		correct = 0
		for y in range(0, len(grid)):
			if y < mirror_y:
				reflect_y = y + 2 * (mirror_y - y) - 1
			else:
				reflect_y = y - (2 * (y - mirror_y) + 1)
			for x in range(0, len(grid[0])):				
				if in_bounds(grid, x, reflect_y):
					#print(f"comparing at x={x}, y={(y, reflect_y)}: {grid[reflect_y][x]} <=> {grid[y][x]}")
					if grid[reflect_y][x] != grid[y][x]:
						valid = False
					else:
						correct += 1
				else:
					correct += 1
		
		#print(f"{correct} ")
		if correct == len(grid) * len(grid[0]) - 2:
			vertical_mirrors.append(mirror_y)
	
	for mirror_x in range(1, len(grid[0])):
		# print(f" testing x={mirror_x}")
		valid = True
		correct = 0
		for x in range(0, len(grid[0])):
			if x < mirror_x:
				reflect_x = x + 2 * (mirror_x - x) - 1
			else:
				reflect_x = x - (2 * (x - mirror_x) + 1)
			for y in range(0, len(grid)):				
				if in_bounds(grid, reflect_x, y):
					#print(f"comparing at x={(x, reflect_x)}, y={y}: {grid[y][x]} <=> {grid[y][reflect_x]}")
					if grid[y][reflect_x] != grid[y][x]:
						valid = False
					else:
						correct += 1
				else:
					correct += 1
		#print(f"{correct} ")
		if correct == len(grid) * len(grid[0]) - 2:
			horizontal_mirrors.append(mirror_x)
					
grid = []

while True:
	try:
		line = input()
		if len(line.strip()) > 0:
			grid.append(line)
		else:
			print(f"processing grid... h x w = {len(grid)} x {len(grid[0])}")
			process(grid)
			grid = []
	except EOFError:
		print(f"processing grid... h x w = {len(grid)} x {len(grid[0])}")
		process(grid)
		grid = []
		break
		
print(f"sum: {sum([100 * vm for vm in vertical_mirrors] + horizontal_mirrors)}")
