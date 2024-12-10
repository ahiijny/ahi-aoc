from collections import deque

grid = []
starts = []


try:
	while True:
		grid.append([int(a) for a in input()])
except EOFError:
	pass
	
for y in range(len(grid)):
	for x in range(len(grid[0])):
		if grid[y][x] == 0:
			starts.append((x,y))
	
print(grid)
print(f"starts: {starts}")

# dfs

q = deque()

for s in starts:
	q.append([s])
	
def bounds(p):
	return 0 <= p[0] and p[0] < len(grid[0]) and 0 <= p[1] and p[1] < len(grid)
	
dirs = [
	(1, 0),
	(0, 1),
	(-1, 0),
	(0, -1)
]

def add(a, b):
	return (a[0] + b[0], a[1] + b[1])
	
routes = set()
ends = set()

while len(q) > 0:
	p = q.pop()
	loc = p[-1]
	
	for d in dirs:
		l2 = add(loc, d)		
		if bounds(l2):
			if grid[l2[1]][l2[0]] != grid[loc[1]][loc[0]] + 1:
				continue
			if grid[l2[1]][l2[0]] == 9:
				routes.add(tuple(p + [l2]))
				ends.add((p[0], l2))
			else:
				p2 = p + [l2]
				q.append(p2)
	
print(f"routes: {routes}")
print(len(routes))
