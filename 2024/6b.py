grid = []
visited = {}

dirs = [
	(0, -1),
	(1, 0),
	(0, 1),
	(-1, 0)
	]
di = 0
start = None

with open('6.in') as f:
	for y, line in enumerate(f):
		grid.append(line.strip())
		for x, p in enumerate(grid[y]):
			if p == '^':
				start = (x, y)
				
def bounded(x, y):
	return 0 <= x and x < len(grid[0]) and 0 <= y and y < len(grid)
print(grid)
  

n = 0
blocks = set()

for y in range(len(grid)):
	for x in range(len(grid[0])):
		if x == 0:
			print(f"check x={x}, y={y}")
		if grid[y][x] == '#': continue
		if (x,y) == start: continue
		
		grid2 = [[p for p in row] for row in grid]
		grid2[y][x] = '#'
		di = 0
		
		v2 = {}
		
		p = start
		loop = False
		while bounded(*p):
			d = dirs[di]
			if (p, di) in v2:
				loop = True
				break
			v2[(p, di)] = True
			p2 = (p[0] + d[0], p[1]+d[1])
			if not bounded(*p2):
				break
			if grid2[p2[1]][p2[0]] == '#':
				di = (di + 1) % 4
				continue
			p = p2
		if loop:
			n += 1
			blocks.add((x,y))
			
print(n)
		
for y in range(len(grid)):
	for x in range(len(grid[0])):
		if (x,y) in blocks:
			print("O", end="")
		else:
			print(grid[y][x], end="")
	print()
