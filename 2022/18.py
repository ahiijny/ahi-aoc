from collections import deque

grid = {}

while True:
	try:
		vox = tuple(int(d) for d in input().split(','))
		grid[vox] = True
	except EOFError:
		break

# count surface area

print(f"voxels: {grid}")

total_area = 0

for x, y, z in grid.keys():
	sides = 6
	if (x-1, y, z) in grid: sides -= 1
	if (x+1, y, z) in grid: sides -= 1
	if (x, y-1, z) in grid: sides -= 1
	if (x, y+1, z) in grid: sides -= 1
	if (x, y, z-1) in grid: sides -= 1
	if (x, y, z+1) in grid: sides -= 1
	
	total_area += sides
	
print(f"total area: {total_area}")

