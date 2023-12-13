from collections import deque

grid = []
adj = {}

while True:
	try:
		line = input()
		grid.append(line)
	except EOFError:
		break
		
print(f"grid={grid}")

# calc adjacency

start = None

def in_bounds(x, y):
	if 0 <= x and x < len(grid[0]) and 0 <= y and y < len(grid):
		return True
	return False

for y in range(len(grid)):
	for x in range(len(grid[0])):
		adj[(x,y)] = set()
		
for y in range(len(grid)):
	for x in range(len(grid[0])):
		ch = grid[y][x]
		ns = [] # neighbours
		if ch == '.':
			pass
		elif ch == '|':
			ns.append((x, y-1))
			ns.append((x, y+1))
		elif ch == '-':
			ns.append((x-1, y))
			ns.append((x+1, y))
		elif ch == 'L':
			ns.append((x, y-1))
			ns.append((x+1, y))
		elif ch == 'J':
			ns.append((x, y-1))
			ns.append((x-1, y))
		elif ch == '7':
			ns.append((x-1, y))
			ns.append((x, y+1))
		elif ch == 'F':
			ns.append((x, y+1))
			ns.append((x+1, y))
		elif ch == 'S':
			start = (x, y)			
		for n in ns:
			(x2, y2) = n
			if in_bounds(x2, y2):
				adj[(x, y)].add((x2, y2))
			
# prune non-reciprocal
for y in range(len(grid)):
	for x in range(len(grid[0])):
		ns = adj[(x,y)]
		n2s = set()
		for n in ns:
			if (x,y) in adj[n]:
				n2s.add(n)
			elif grid[n[1]][n[0]] == 'S':
				n2s.add(n)
				adj[n].add((x,y))
		adj[(x,y)] = n2s
				
print(f"adj={adj}")

dists = {}
dists[start] = 0

# walk bfs

q = deque()
q.append((start, 0))

while len(q) > 0:
	p, d = q.popleft()
	if p not in dists or dists[p] > d:
		dists[p] = d
	for n in adj[p]:
		if n not in dists or dists[n] > d+1:
			q.append((n, d+1))
			dists[n] = d+1
			
# print(f"dists={dists}")

for y in range(len(grid)):
	for x in range(len(grid[0])):
		if (x,y) in dists:
			print('{0:<3}'.format(dists[(x,y)]), end='')
		else:
			print('{0:<3}'.format('.'), end='')
	print()
print(f"max_dist={max(dists.values())}")


# walk countour
# arbitrarily pick one, it will be either clockwise or counterclockwise

choices = list(adj[start])

path = [start, choices[0]]
cur = choices[0]
prev = start
lefts = 0
rights = 0
prev_delta = (cur[0]-start[0], cur[1]-start[1])

while cur != start:
	choices = list(adj[cur])
	n = choices[0]
	if choices[0] == prev:
		n = choices[1]
		
	delta = (n[0]-cur[0], n[1]-cur[1])
	path.append(n)
	prev = cur
	cur = n
	prev_delta = delta

print(f"loop={path}")
print(f"tour len={len(path)}")

# https://en.wikipedia.org/wiki/Even%E2%80%93odd_rule

delta = 0.5

edge_crosses = {}

for i in range(len(path)-1): # start and end point will repeat
	e1 = path[i]
	e2 = path[i+1]
	
	x1 = min(e1[0], e2[0])
	x2 = max(e1[0], e2[0])
	y1 = min(e1[1], e2[1])
	y2 = max(e1[1], e2[1])
	if x1 == x2:
		edge_crosses[(x1, y1+0.5)] = True

def is_on_edge(x, y):
	if (x,y) in edge_crosses:
		return True
	return False
	
# short horizontal rays

crosses = []

for y in range(len(grid)):
	print(f"raytesting y={y}")
	num_crosses = 0
	crosses.append([])
	for x in range(len(grid[0])):
		if is_on_edge(x, y+0.5):
			num_crosses += 1
		crosses[-1].append(num_crosses)
		
path_set = set(path)

num_inside = 0

def print_insides():
	for y, r in enumerate(crosses):
		for x, c in enumerate(r):
			if (x,y) in path_set:
				print('{0:<3}'.format('+'), end='')
			else:
				print('{0:<3}'.format(c), end='')
		print()

for y, r in enumerate(crosses):
	for x, c in enumerate(r):
		if c % 2 == 1 and (x,y) not in path_set:
			num_inside += 1
print_insides()

print(f"num_inside={num_inside}")
		