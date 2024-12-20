import heapq

dirs = [
	(-1, 0),
	(0, -1),
	(1, 0),
	(0,1)
]
	
grid = []
S = None
E = None

def bounds(x, y):
	return 0 <= x and x < len(grid[0]) and 0 <= y and y < len(grid)
	
def add(p1, p2):
	return (p1[0] + p2[0], p1[1] + p2[1])
	
def mul(p, s):
	return (p[0] * s, p[1] * s)

try:
	while True:
		grid.append(input())
except EOFError:
	pass
	
H = len(grid)
W = len(grid[0])
	
for y in range(H):
	for x in range(W):
		if grid[y][x] == 'S':
			start = (x,y)
		elif grid[y][x] == 'E':
			end = (x,y)
			
def best_time(grid, start, end, stop_after=999999):
	#print(f"best_time(start={start},end={end}")
	q = []
	heapq.heapify(q)
	q.append((0, [start]))
	best = {}
	while len(q) > 0:
		cost, route = heapq.heappop(q)
		if cost > stop_after:
			print(f"stopping early after cost={cost}")
			return None, None
		p = route[-1]
		best[p] = cost
		if p == end:
			return cost, route
			print(f"cost={cost}")
		for d in dirs:
			p2 = add(p, d)
			c2 = cost + 1
			if bounds(*p2) and grid[p2[1]][p2[0]] != '#' and (p2 not in best or best[p2] > c2):
				r2 = route + [p2]
				heapq.heappush(q, (c2, r2))
	return None, None

def print_grid():
	for y in range(H):
		for x in range(W):
			print(grid[y][x], end='')
		print()

print_grid()
base_cost, base_route = best_time(grid, start, end)

check_dirs = [
	(0,0),
	(1,0),
	(0,1)
]

times = {}
count_over_100 = 0

for y in range(H):
	for x in range(W):
		print(f"checking cheats for ({x},{y})...")
		grid2 = [[grid[v][u] for u in range(W)] for v in range(H)]
		if not grid[y][x] == '#':
			continue
		grid2[y][x] = '.'
		for d in check_dirs:
			c2 = add((x,y), d)
			if not bounds(*c2):
				continue
			if not grid[c2[1]][c2[0]] == '#':
				continue
			grid2[c2[1]][c2[0]] = '.'
			cost, route = best_time(grid2, start, end, base_cost-100)
			if cost is None:
				continue
			times[(x, y, d)] = cost
			improvement = base_cost - cost
			if improvement >= 100:
				count_over_100 += 1

print(count_over_100)

print(count_over_100)

		