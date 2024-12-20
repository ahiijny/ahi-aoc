import heapq

H = W = 71
n = 1024

dirs = [
	(-1, 0),
	(0, -1),
	(1, 0),
	(0,1)
]
	
grid = []
start = (0,0)
end = (W-1,H-1)
blocks = []

def bounds(x, y):
	return 0 <= x and x < len(grid[0]) and 0 <= y and y < len(grid)
	
def add(p1, p2):
	return (p1[0] + p2[0], p1[1] + p2[1])
	
def mul(p, s):
	return (p[0] * s, p[1] * s)
	
try:
	while True:
		blocks.append(tuple(int(a) for a in input().split(",")))
except EOFError:
	pass

grid = [['.' for x in range(W)] for y in range(H)]
	
for i, b in enumerate(blocks):
	grid[b[1]][b[0]] = '#'
	if i == n-1:
		break

# cost, route
best_cost = None
best = {}
state = (0, [(start)])
q = [state]

heapq.heapify(q)
best_route = None
while len(q) > 0:
	cost, route = heapq.heappop(q)
	p = route[-1]
	if p == end:
		best_cost = cost
		best_route = route
		break
	if best_cost is not None and cost > best_cost:
		break
	for d in dirs:
		p2 = add(p, d)
		if bounds(*p2) and grid[p2[1]][p2[0]] != '#' and p2 not in route:
			c2 = cost + 1
			r2 = route + [p2]
			if p2 not in best or best[p2] > c2:
				best[p2] = c2
				heapq.heappush(q, (c2, r2))
				
				
def print_grid(br):
	p = set(br)
	for y in range(H):
		for x in range(W):
			if (x,y) in p:
				print('O', end='')
			else:
				print(grid[y][x], end='')
		print()

print_grid(best_route)
print(f"solution: cost={best_cost}, route={best_route}")