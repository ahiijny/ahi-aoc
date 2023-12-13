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
	if delta != prev_delta:
		if prev_delta == (1, 0):
			if delta == (0, 1):
				rights += 1
			elif delta == (0, -1):
				lefts += 1
		elif prev_delta == (0, -1):
			if delta == (1, 0):
				rights += 1
			elif delta == (-1, 0):
				lefts += 1
		elif prev_delta == (-1, 0):
			if delta == (0, -1):
				rights += 1
			elif delta == (0, 1):
				lefts += 1
		elif prev_delta == (0, 1):
			if delta == (-1, 0):
				rights += 1
			elif delta == (1, 0):
				lefts += 1
	path.append(n)
	prev = cur
	cur = n
	prev_delta = delta

print(f"loop={path}")
print(f"tour len={len(path)}")
print(f"left turns={lefts}, right turns={rights}")
if rights > lefts:
	print("> clockwise")
else:
	print("> counterclockwise")
	path = path[::-1]
	
	print("reversing path for consistency")
	print(f"path={path}")
	
# do clockwise
# in a clockwise walk, inside is on the right

blots = set()

for i, cur in enumerate(path):
	if i == 0:
		continue
	delta = (path[i][0] - path[i-1][0], path[i][1] - path[i-1][1])
	prev_delta = None
	if i > 1:
		prev_delta = (path[i-1][0] - path[i-2][0], path[i-1][1] - path[i-2][1])
	right = None
	if delta == (1, 0):
		right = (0, 1)
	elif delta == (0, 1):
		right = (-1, 0)
	elif delta == (-1, 0):
		right = (0, -1)
	elif delta == (0, -1):
		right = (0, 1)
	
	to_add = [(cur[0] + right[0], cur[1] + right[1])]
		
	for blot in to_add:
		if in_bounds(*blot) and blot not in path:
			blots.add(blot)
			

delta = [(1, 0), (0, 1), (-1, 0), (0, -1)]

# paint fill
q = deque(list(blots))

while len(q) > 0:
	p = q.popleft()
	for d in delta:
		p2 = (p[0] + d[0], p[1] + d[1])
		if in_bounds(*p2) and p2 not in blots and p2 not in path:
			blots.add(p2)
			q.append(p2)
			
		
for y in range(len(grid)):
	for x in range(len(grid[0])):
		if (x,y) in blots:
			print('{0:<1}'.format('I'), end='')
		elif (x,y) in path:
			print('{0:<1}'.format('+'), end='')
		else:
			print('{0:<1}'.format('O'), end='')
	print()

print(f"num insides={len(blots)}")