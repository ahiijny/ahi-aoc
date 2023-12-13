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

		