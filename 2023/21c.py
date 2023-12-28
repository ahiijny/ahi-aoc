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

def unconvert(u, p):
	return (W * u[0] + p[0], H * u[1] + p[1])

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

steps = 150

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

looping_metaboards = {}

def find_equiv_index(a, b, i):
	"""
	for a loop where [a, b] and state[a] === state[b],
		e.g. 2<->5
		2,3,4,5(2),6(3)
	state is i % (b-a)
	"""
	if i < b:
		return i
	return i % (b-a) + a

for i in range(steps):
	next_locs = set()
	next_locs_by_board = {}
	for u, locs in locs_by_board.items():
		if u in looping_metaboards:
			a,b = looping_metaboards[u]
			i0 = find_equiv_index(a, b, i)
			print(f"reusing looping metaboard {u}@{i0}")
			sublocs = {unconvert(u, p) for p in i_to_state[i0][u]}
			next_locs.update(sublocs)
			next_locs_by_board[u] = sublocs
		else:
			for loc in locs:
				loc = unconvert(u, loc)
				for adj in adjs:
					p2 = add(loc, adj)
					minx = min(minx, p2[0])
					maxx = max(maxx, p2[0])
					miny = min(miny, p2[1])
					maxy = max(maxy, p2[1])
					
					u2, ep = convert(*p2)
					#print(f"{p2} -> universe = {u2}, equiv_point = {p2}")
					if u2 not in next_locs_by_board:
						next_locs_by_board[u2] = set()
					if p2 not in all_locs:
						if grid(*p2) != '#':
							next_locs_by_board[u2].add(ep)
							next_locs.add(p2)
	all_locs = next_locs
	locs_by_board = next_locs_by_board
	print(f"{i} steps: {len(locs_by_board)} metaboards, bounding box: {(minx, miny)} -> {(maxx, maxy)}, reachable = {len(all_locs)}")
	
	print_metaboards()
	
	# record state hists
	
	i_to_state[i] = {}
	
	for u, locs in locs_by_board.items():
		state = frozenset(locs)
		i_to_state[i][u] = state
		
		if state in state_hist:
			u_to_iis = state_hist[state]
			u2, i2 = next(iter(u_to_iis.items()))
			statestr = "" if len(state) > 5 else str(state)
			if u not in u_to_iis:
				u_to_iis[u] = []
			if len(u_to_iis[u]) < 2:
				print(f"recurring state: metaboard {u}@{i} steps matches metaboard {u2}@{i2} steps: {statestr}")
				u_to_iis[u].append(i)
				if len(u_to_iis[u]) == 2:
					print(f"stable loop found for metaboard {u}")
					looping_metaboards[u] = tuple(u_to_iis[u])
			
		else:
			state_hist[state] = {u: [i]}
	
	if len(all_locs) < 1000:
		print_grid(i + 4)
	

print(f"num visited: {len(all_locs)}")
