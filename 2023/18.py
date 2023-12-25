instrs = []
grid = {}
p = (0, 0)
grid[p] = True

while True:
	try:
		i = input().split()
		instrs.append([i[0], int(i[1]), i[2][1:-1]])
	except EOFError:
		break
		
print(f"instrs: {instrs}")

deltas = {
	'U': (0, -1),
	'R': (1, 0),
	'D': (0, 1),
	'L': (-1, 0)
}

def add(a, b):
	return (a[0] + b[0], a[1] + b[1])

for instr in instrs:
	face, dist, col = instr
	for i in range(dist):
		p = add(p, deltas[face])
		grid[p] = True
		
def bounds():
	minx = min(p[0] for p in grid)
	maxx = max(p[0] for p in grid)
	miny = min(p[1] for p in grid)
	maxy = max(p[1] for p in grid)
	
	return minx, maxx, miny, maxy
	
fills = {}
		
def print_grid():
	minx, maxx, miny, maxy = bounds()	
	
	for y in range(miny, maxy+1):
		for x in range(minx, maxx+1):
			if (x,y) in grid:
				print('#', end='')
			elif (x,y) in fills:
				print('O', end='')
			else:
				print('.', end='')
		print()
		
# fill in edges

minx, maxx, miny, maxy = bounds()

# https://en.wikipedia.org/wiki/Point_in_polygon
# consider vertices on the ray as lying slightly above the ray.

for y in range(miny, maxy+1):
	crosses = 0
	# ray trace left to right
	for x in range(minx, maxx+1):
		if (x,y) in grid and (x,y+1) in grid:
			crosses += 1
		if crosses % 2 == 1:
			fills[(x,y)] = True
	
print_grid()

dug = {**grid, **fills}

print(f"volume = {len(dug)}")