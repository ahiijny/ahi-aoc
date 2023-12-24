from collections import deque

grid = []

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

# dfs

q = deque()
q.append((start, {start: 0}))

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
		if in_bounds(p2):
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


best_length = 0

while len(q) > 0:
	p, path = q.popleft()
	#print(f"checking p={p}, path len = {len(path)}")
	prev = None
	if len(path) > 1:
		prev = next(reversed(path))
	adjs = get_adjs(p)
	required_next = None
	if prev is not None:
		prev_gr = grid[prev[1]][prev[0]]
		if prev_gr in slope_delta:
			required_next = add(p, slope_delta[prev_gr])
	
	for p2 in adjs:
		if p2 in path:
			continue
		if required_next is not None and p2 != required_next:
			continue
		if grid[p2[1]][p2[0]] == '#':
			continue
		path2 = dict(path)
		path2[p2] = len(path)
		if p2 == end:
			print(f"found end with length = {len(path)}")
			if len(path) > best_length:
				best_length = len(path)
		else:
			q.appendleft((p2, path2))
			
print(f"best length: {best_length}")
		