from collections import deque

grid = []

while True:
	try:
		grid.append(input())
	except EOFError:
		break
		
start = None

for y in range(len(grid)):
	for x in range(len(grid[0])):
		if grid[y][x] == 'S':
			start = (x,y)
			break

visited = {}

q = deque()
q.appendleft((start, 0))

adjs = [
	(1, 0),
	(0, 1),
	(-1, 0),
	(0, -1)
]

def add(a, b):
	return (a[0] + b[0], a[1] + b[1])

def in_bounds(p):
	return 0 <= p[0] and p[0] < len(grid[0]) and 0 <= p[1] and p[1] < len(grid)

# bfs

steps = 55

locs = set()
locs.add(start)

for i in range(steps):
	next_locs = set()
	for loc in locs:
		for adj in adjs:
			p2 = add(loc, adj)
			if in_bounds(p2) and grid[p2[1]][p2[0]] != '#':
				next_locs.add(p2)
	locs = next_locs
	
for y in range(len(grid)):
	for x in range(len(grid[0])):
		if (x,y) in locs:
			print('O', end='')
		else:
			print(grid[y][x], end='')
	print()

print(f"num visited: {len(locs)}")

# calc min dists