import heapq

def bounds(x, y):
	return 0 <= x and x < len(grid[0]) and 0 <= y and y < len(grid)
	
def add(p1, p2):
	return (p1[0] + p2[0], p1[1] + p2[1])
	
def mul(p, s):
	return (p[0] * s, p[1] * s)
	
grid = []
start = None
end = None

dirs = {
	0: (-1, 0),
	1: (0, -1),
	2: (1, 0),
	3: (0,1)
}

try:
	while True:
		grid.append([c for c in input()])
except EOFError:
	pass
	
H = len(grid)
W = len(grid[0])
	
def print_grid():
	for y in range(H):
		for x in range(W):
			print(grid[y][x], end='')
		print()
		
print_grid()

for y in range(H):
	for x in range(W):
		if grid[y][x] == 'S':
			start = (x,y)
		elif grid[y][x] == 'E':
			end = (x,y)

best = {}
best[(start, 2)] = 0

# cost, direction, route
state = (0, 2, [(start)])
q = [state]
heapq.heapify(q)
best_routes = []
sits = set()
best_cost = None

while len(q) > 0:
	cost, face, route = heapq.heappop(q)
	if best_cost is not None and cost > best_cost:
		break
	p = route[-1]
	if grid[p[1]][p[0]] == 'E':
		print(f'lowest cost route: face={face}, route={route}\nc={cost}')
		sits.update(route)
		if best_cost is None:
			best_cost = cost
	
	if (p, face) not in best:
		best[(p, face)] = cost
	elif best[(p, face)] < cost:
		continue
	
	# find neighbours
	# 2 rotations
	c2 = cost+1000
	f2 = (face + 1) % 4
	r2 = route
	if (p, f2) not in best or best[(p, f2)] >= c2:
		heapq.heappush(q, (c2, f2, route))
	f2 = (face - 1) % 4
	if (p, f2) not in best or best[(p, f2)] >= c2:
		heapq.heappush(q, (c2, f2, route))
	
	# 1 advance
	n = add(p, dirs[face])
	if grid[n[1]][n[0]] != '#':
		c2 = cost+1
		f2 = face
		r2 = route + [n]
		if (n, f2) not in best or best[(n, f2)] >= c2:
			heapq.heappush(q, (c2, face, r2))

for y in range(H):
	for x in range(W):
		if (x,y) in sits:
			print("O", end='')
		else:
			print(grid[y][x], end='')
	print()

print(sits)
print(len(sits))
