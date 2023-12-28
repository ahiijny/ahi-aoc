from collections import deque

core_grid = []

while True:
	try:
		core_grid.append(input())
	except EOFError:
		break
		
start = None

for y in range(len(core_grid)):
	for x in range(len(core_grid[0])):
		if core_grid[y][x] == 'S':
			start = (x,y)
			break

q = deque()
q.appendleft((start, 0))

adjs = [
	(1, 0),
	(0, 1),
	(-1, 0),
	(0, -1)
]

W = len(core_grid[0])
H = len(core_grid)

state_hist = {} # record duplicate states in repeated boards; 

def convert(x, y):
	"""
		e.g. board
		
		  0 1 2 3 4
		0 . . . . .
		1 . . . x .
		2 . . . . .
		3 . x . x .
		4 . . . . .
		
		
		board repeats horizontally and vertically
		
		so (0,0) = (5,0) = (5,5) = (-5, 0) = (-5, -5)
		
		python modulo -4 % 5 -> 1, -6 % 5 -> 4, so it works correctly 
		
	"""
	equiv_x = x % W
	equiv_y = y % H
	
	univ_x = x // W  # mario parallel universes
	univ_y = y // H
	return ((univ_x, univ_y), (equiv_x, equiv_y))
	
def grid(x, y):
	u, p = convert(x,y)
	return core_grid[p[1]][p[0]]
	

def add(a, b):
	return (a[0] + b[0], a[1] + b[1])

# bfs

state_to_i = {} # map from metaboard state to list of -> (metaboard coords, step) occurrences
i_to_state = {}

steps = 300

all_locs = set()
all_locs.add(start)
locs_by_board = {  # coordinates of metaboard -> list of reachable points inside
	(0,0): set()
}
locs_by_board[(0,0)].add(start)

def print_grid(radius):
	startx = W // 2 - radius
	endx = W // 2 + radius + 1
	starty = H // 2 - radius
	endy = H // 2 + radius + 1
	for y in range(starty, endy):
		for x in range(startx, endx):
			if (x,y) in locs:
				print('O', end='')
			else:
				print(grid(x,y), end='')
		print()

minx = start[0]
maxx = start[0]
miny = start[1]
maxy = start[1]

shockwave = set()
shockwave.add(start)

def print_metaboards():
	minx = None
	maxx = None
	miny = None
	maxy = None
	
	for u in locs_by_board:
		minx = u[0] if minx is None else min(minx, u[0])
		maxx = u[0] if maxx is None else max(maxx, u[0])
		miny = u[1] if miny is None else min(miny, u[1])
		maxy = u[1] if maxy is None else max(maxy, u[1])
		
	print(f"metaboards range: {(minx, miny)} -> {(maxx, maxy)}")
	for y in range(miny, maxy + 1):
		for x in range(minx, maxx + 1):
			print(f"{str(len(locs_by_board.get((x,y), set()))):<4}", end=' ')
		print()
			
	

for i in range(steps):
	next_locs = set()
	
	for loc in shockwave:
		for adj in adjs:
			p2 = add(loc, adj)
			minx = min(minx, p2[0])
			maxx = max(maxx, p2[0])
			miny = min(miny, p2[1])
			maxy = max(maxy, p2[1])
			
			u, ep = convert(*p2)
			#print(f"{p2} -> universe = {u}, equiv_point = {p2}")
			if u not in locs_by_board:
				locs_by_board[u] = set()
			locs_by_board[u].add(ep)
			if p2 not in all_locs:
				if grid(*p2) != '#':
					next_locs.add(p2)
	
	shockwave = next_locs
	all_locs.update(next_locs)
	print(f"{i} steps: {len(locs_by_board)} metaboards, bounding box: {(minx, miny)} -> {(maxx, maxy)}, visited = {len(all_locs)}")
	
	print_metaboards()
	
	# record state hists
	
	i_to_state[i] = {}
	
	for u, locs in locs_by_board.items():
		state = frozenset(locs)
		i_to_state[i][u] = state
		
		if state in state_hist:
			u_to_iis = state_hist[state]
			u2, i2 = next(iter(u_to_iis.items()))
			if u not in u_to_iis:
				print(f"recurring state: metaboard {u}@{i} steps matches metaboard {u2}@{i2} steps")
				u_to_iis[u] = i
		else:
			state_hist[state] = {u: i}
	
	if i % 8 == 1:
		pass
		# print_grid(i + 4)
	

print(f"num visited: {len(all_locs)}")
