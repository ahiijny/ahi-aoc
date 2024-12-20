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
	q.append((0, [start], []))
	best = {}
	solutions = []
	count = 0
	while len(q) > 0:
		count += 1
		cost, route, cheats = heapq.heappop(q)
		if count % 1 == 0:
			print(f"checking cost={cost}, cheats={cheats} count={count}")
		p = route[-1]
		best[(p, len(cheats))] = cost
		if p == end:
			solutions.append((cost, route, cheats))
			if len(cheats) == 0:
				return solutions
		for d in dirs:
			p2 = add(p, d)
			c2 = cost + 1
			if bounds(*p2):
				if (p2, len(cheats)) not in best or best[(p2, len(cheats))] >= c2:
					cheats2 = cheats
					if grid[p2[1]][p2[0]] == '#':
						if len(cheats) == 0:
							cheats2 = [p2]
						elif len(cheats) == 1 and (cheats[0][0] == p2[0] and abs(cheats[0][1] - p2[1]) == 1 or cheats[0][1] == p2[1] and abs(cheats[0][0] - p2[0]) == 1):
							cheats2 = cheats + [p2]
						else:
							continue
					r2 = route + [p2]
					heapq.heappush(q, (c2, r2, cheats2))
	return None, None

def print_grid():
	for y in range(H):
		for x in range(W):
			print(grid[y][x], end='')
		print()

print_grid()
solutions = best_time(grid, start, end)
base_cost, base_route, base_cheats = solutions[-1]
threshold = 100
count = 0
print("solutions:")
for soln in solutions:
	print(f"cost={soln[0]}, cheats={soln[2]}")
	if base_cost - soln[0] >= threshold:
		count += 1
		
print(f"total unique cheats with improvement > {threshold}: {count}")
	
