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
			
def best_time(grid, start, end):
	#print(f"best_time(start={start},end={end}")
	q = []
	heapq.heapify(q)
	q.append((0, [start]))
	best = {}
	while len(q) > 0:
		cost, route = heapq.heappop(q)
		p = route[-1]
		best[p] = cost
		if p == end:
			return cost, route, best
			print(f"cost={cost}")
		for d in dirs:
			p2 = add(p, d)
			c2 = cost + 1
			if bounds(*p2) and grid[p2[1]][p2[0]] != '#' and (p2 not in best or best[p2] > c2):
				r2 = route + [p2]
				heapq.heappush(q, (c2, r2))
	return None, None, best

def print_grid():
	for y in range(H):
		for x in range(W):
			print(grid[y][x], end='')
		print()

print_grid()
base_cost, base_route, best = best_time(grid, start, end)

print(f"best = {best}")

end_cheats = [
	(1,0),
	(0,1),
	(-1,0),
	(0, -1)
]
over_100 = 0

cheatlist = []
for y in range(H):
	for x in range(W):
		print(f"checking cheats at ({x},{y})...")
		c1 = (x,y)
		if grid[c1[1]][c1[0]] != '#':
			continue
		for d in end_cheats:
			c2 = add(c1, d)
			if not bounds(*c2):
				continue
			if c2 not in best:
				continue
			if grid[c2[1]][c2[0]] != '.':
				continue
			# check all possible entrypoints and all possible entrypoints
			best_improvement = None
			for entry_d in dirs:
				c0 = add(c1, entry_d)
				if c0 == c2:
					continue
				if not bounds(*c0):
					continue
				if grid[c0[1]][c0[0]] == '#':
					continue
				if c0 not in best:
					continue
				cheat_improvement = best[c2] - best[c0] - 2
				if best_improvement is None and cheat_improvement > 0 or best_improvement is not None and cheat_improvement > best_improvement:
					best_improvement = cheat_improvement
			if best_improvement is not None:
				print(f"cheat {c1} -> {c2}: best improvement = {best_improvement}")
				cheatlist.append((best_improvement, c1, c2))
				if best_improvement >= 100:
					over_100 += 1
			
print("cheats:")
for c in sorted(cheatlist, reverse=True):
	print(f"  {c[0]} <- {c[1]}..{c[2]}")
print(over_100)
