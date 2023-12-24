from collections import deque

grid = []
adjs_cache = {}

while True:
	try:
		grid.append(input())
	except EOFError:
		break

print(grid)

branch_counter = 0

start = (grid[0].index('.'), 0)
end = (grid[-1].index('.'), len(grid)-1)

print(f"start={start}, end={end}")

def in_bounds(p):
	return 0 <= p[0] and p[0] < len(grid[0]) and 0 <= p[1] and p[1] < len(grid)
	
deltas = [
	(1, 0),
	(0, 1),
	(-1, 0),
	(0, -1)
]
	
def get_adjs(p):
	adjs = []
	for d in deltas:
		p2 = add(p, d)
		if in_bounds(p2) and grid[p2[1]][p2[0]] != '#':
			adjs.append(p2)
	return adjs
	
def add(a, b):
	return (a[0] + b[0], a[1] + b[1])
	
slope_delta = {
	'^': (0, -1),
	'>': (1, 0),
	'v': (0, 1),
	'<': (-1, 0)
}

path_count = 0

adj_hist = {}

for y in range(len(grid)):
	for x in range(len(grid[0])):
		if grid[y][x] != '#':
			adjs = get_adjs((x,y))
			adjs_cache[(x,y)] = adjs
			if len(adjs) in adj_hist:
				adj_hist[len(adjs)] += 1
			else:
				adj_hist[len(adjs)] = 1	
			path_count += 1
		
print(f"adj counts: {adj_hist}")
		
# construct graph with dfs

# dfs

visited = {}
seen = {}
nodes = {
	start: set(),
	end: set()
}

edges = {}

q = deque()
q.append((start, {start: True}, start, 0)) # cur_node, path, prev_node, dist_to_prev_node

while len(q) > 0:
	p, path, prev_node, dist = q.popleft()
	seen[p] = True
	#print(f"checking {p}, prev_node={prev_node}, dist={dist}")
	
	adjs = adjs_cache[p]
	if len(adjs) > 2 or p == end: # new node
		print(f"node @ {p}")
		if p not in nodes:
			nodes[p] = set()
		nodes[p].add(prev_node)
		nodes[prev_node].add(p)
		edges[(p, prev_node)] = dist
		edges[(prev_node, p)] = dist
		
		prev_node = p
		path = {p: True}
		dist = 0
	if p in visited:
		continue
	for adj in adjs:
		if adj not in path:
			path2 = dict(path)
			path2[adj] = True
			q.appendleft((adj, path2, prev_node, dist + 1))
	if len(adjs) > 2 or p == end:
		visited[p] = True

print(f"nodes: {nodes}")
print(f"edges: {edges}")

print(f"max connected = {max(len(n) for n in nodes.values())}")
print(f"path_count = {path_count}")
print(f"walked locations = {len(seen)}")

for y in range(len(grid)):
	for x in range(len(grid[0])):
		if (x,y) in nodes:
			print("O", end='')
		else:
			print(grid[y][x], end='')
	print()


# dfs

q = deque()
q.append((start, {start: 0}, 0))
c = 0
best_length = 0

while len(q) > 0:
	p, path, dist = q.popleft()
	c += 1
	#print(f"checking p={p}, path len = {dist}, q = {len(q)}, options = {len(nodes[p])}")
	
	for p2 in nodes[p]:
		if p2 in path:
			continue
			
		path2 = dict(path)
		path2[p2] = len(path)
		dist2 = dist + edges[(p, p2)]
		if p2 == end:
			print(f"found end with length = {dist2}\tnodes in path={len(path)}\tbest = {best_length}\tq = {len(q)}\tnodes checked={c}")
			if dist2 > best_length:
				best_length = dist2
		else:
			q.appendleft((p2, path2, dist2))
			
print(f"best length: {best_length}")