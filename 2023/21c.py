from collections import deque

steps = 427
N = [6, 10, 50, 100, 500, 1000, 5000, 26501365]

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

for i in range(1, steps+1):
	next_locs = set()
	next_locs_by_board = {}
	for u, locs in locs_by_board.items():
		if False: #u in looping_metaboards:
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

# use recurrence to calculate steps

def calc_reachable(n):	
	# diamond steady state
	
	# note this code doesnt work correctly, see 21d.py for correct version

	
	"""
	
	example:
	
	457 steps: 37 metaboards, bounding box: (-393, -393) -> (523, 523), reachable = 188858
	metaboards range: (-3, -3) -> (3, 3)
	0    0    966  5820 972  0    0
	0    966  6749 7712 6746 972  0
	966  6749 7712 7675 7712 6746 972
	5792 7712 7675 7712 7675 7712 5794
	995  6718 7712 7675 7712 6723 969
	0    995  6718 7712 6723 969  0
	0    0    995  5766 969  0    0
	
    458 steps: 41 metaboards, bounding box: (-394, -394) -> (524, 524), reachable = 189987
	metaboards range: (-4, -4) -> (4, 4)
	0    0    0    0    1    0    0    0    0
	0    0    0    1018 5878 1023 0    0    0
	0    0    1018 6808 7675 6782 1023 0    0
	0    1018 6808 7675 7712 7675 6782 1023 0
	1    5901 7675 7712 7675 7712 7675 5881 1
	0    995  6805 7675 7712 7675 6811 992  0
	0    0    995  6805 7675 6811 992  0    0
	0    0    0    995  5904 992  0    0    0
	0    0    0    0    1    0    0    0    0
	 
	 
	"""
	
	"""
	note given input will reach exactly the end of the metaboard, so simplying assumption, shape will
	be like the 457 steps but with longer
	there are boards:
	- 7675  - full, start parity 
	- 7712  - full, off-start parity
	- 6749 	- NW inner
	- 966 	- NW outer
	- 5792 	- W
	- 6718 	- SW inner
	- 995 	- SW outer
	- 5766 	- S
	- 6723 	- SE inner
	- 969 	- SE outer
	- 5794 	- E
	- 6746 	- NE inner
	- 972 	- NE outer
	- 5820	- N
	"""
	print(f"calculating reachable squares for n={n}")
	
	counts = {}
	amounts = {}
	
	minx = start[0] - n
	maxx = start[0] + n
	miny = start[1] - n
	maxy = start[1] + n
	
	minu0 = minx // W
	maxu0 = maxx // W
	minu1 = miny // H
	maxu1 = maxy // H
	
	# edges
	
	if minu0 < 0: # a unique west board; by symmetry, north, east, and south are unique too
		print(f"	distinct N, E, S, W")
		equiv_u = (-1, 0)
		equiv_i = (n - 65) % W + 65
		amounts['w'] = len(i_to_state[equiv_i][equiv_u])
		counts['w'] = 1
		print(f"        w={amounts['w']}x1")
		
		equiv_u = (0, -1)
		equiv_i = (n - 65) % H + 65
		amounts['n'] = len(i_to_state[equiv_i][equiv_u])
		counts['n'] = 1
		print(f"        n={amounts['n']}x1")
		
		equiv_u = (1, 0)
		equiv_i = (n - 65) % W + 65
		amounts['e'] = len(i_to_state[equiv_i][equiv_u])
		counts['e'] = 1
		print(f"        e={amounts['e']}x1")
		
		equiv_u = (0, 1)
		equiv_i = (n - 65) % H + 65
		amounts['s'] = len(i_to_state[equiv_i][equiv_u])
		counts['s'] = 1
		print(f"        s={amounts['s']}x1")
		
	# outer diagonal
	
	# check bottom right corner of metaboard above left edge
	# if it is in the wavefront, then outer diagonal starts with square above W,
	# inner diagonal starts with square up and to right of W
	
	# if it is not in the wavefront, then outer diagonal starts with square up and to right of W
	# inner diagonal starts with square to right of W
	
	test_u = (minu0, minu1-1)
	test_ep = (W-1, H-1)
	loc = unconvert(test_u, test_ep)
	
	# find taxicab distance 
	d = abs(loc[0] - start[0]) + abs(loc[1] - start[1])
	outer_diag = False
	if d <= n:
		outer_diag = True
		print(f"	diagonal is outer")
		
		# assumption: H = W
		
		num_outer_diagonals = maxu0
		num_inner_diagonals = maxu0 - 1
		
		# outer diagonals
		if num_outer_diagonals > 0:
			print(f"	{num_outer_diagonals} outer diagonals per quadrant")
			equiv_u = (-1, -1)
			equiv_i = (n - 131) % W + 131
			amounts['nw_out'] = len(i_to_state[equiv_i][equiv_u])
			counts['nw_out'] = num_outer_diagonals
			print(f"        nw_out={amounts['nw_out']}x{num_outer_diagonals}")
			
			equiv_u = (1, -1)
			equiv_i = (n - 131) % H + 131
			amounts['ne_out'] = len(i_to_state[equiv_i][equiv_u])
			counts['ne_out'] = num_outer_diagonals
			print(f"        ne_out={amounts['ne_out']}x{num_outer_diagonals}")
			
			equiv_u = (1, 1)
			equiv_i = (n - 131) % W + 131
			amounts['se_out'] = len(i_to_state[equiv_i][equiv_u])
			counts['se_out'] = num_outer_diagonals
			print(f"        se_out={amounts['se_out']}x{num_outer_diagonals}")
			
			equiv_u = (-1, 1)
			equiv_i = (n - 131) % H + 131
			amounts['sw_out'] = len(i_to_state[equiv_i][equiv_u])
			counts['sw_out'] = num_outer_diagonals
			print(f"        sw_out={amounts['sw_out']}x{num_outer_diagonals}")
		
		# inner diagonals
		if num_inner_diagonals > 0:
			print(f"	{num_inner_diagonals} inner diagonals per quadrant")
			equiv_u = (-1, -1)
			equiv_i = (n - 261) % W + 261
			amounts['nw_in'] = len(i_to_state[equiv_i][equiv_u])
			counts['nw_in'] = num_inner_diagonals
			print(f"        nw_in={amounts['nw_in']}x{num_inner_diagonals}")
			
			equiv_u = (1, -1)
			equiv_i = (n - 261) % H + 261
			amounts['ne_in'] = len(i_to_state[equiv_i][equiv_u])
			counts['ne_in'] = num_inner_diagonals
			print(f"        ne_in={amounts['ne_in']}x{num_inner_diagonals}")
			
			equiv_u = (1, 1)
			equiv_i = (n - 261) % W + 261
			amounts['se_in'] = len(i_to_state[equiv_i][equiv_u])
			counts['se_in'] = num_inner_diagonals
			print(f"        se_in={amounts['se_in']}x{num_inner_diagonals}")
			
			equiv_u = (-1, 1)
			equiv_i = (n - 261) % H + 261
			amounts['sw_in'] = len(i_to_state[equiv_i][equiv_u])
			counts['sw_in'] = num_inner_diagonals
			print(f"        sw_in={amounts['sw_in']}x{num_inner_diagonals}")
	else:
		print(f"	diagonal is inner")
	
		# assumption: H = W
		
		num_outer_diagonals = maxu0 - 1
		num_inner_diagonals = maxu0 - 2
		
		# outer diagonals
		if num_outer_diagonals > 0:
			print(f"	{num_outer_diagonals} outer diagonals per quadrant")
			equiv_u = (-1, -1)
			equiv_i = (n - 196) % W + 196
			amounts['nw_out'] = len(i_to_state[equiv_i][equiv_u])
			counts['nw_out'] = num_outer_diagonals
			print(f"        nw_out={amounts['nw_out']}x{num_outer_diagonals}")
			
			equiv_u = (1, -1)
			equiv_i = (n - 196) % H + 196
			amounts['ne_out'] = len(i_to_state[equiv_i][equiv_u])
			counts['ne_out'] = num_outer_diagonals
			print(f"        ne_out={amounts['ne_out']}x{num_outer_diagonals}")
			
			equiv_u = (1, 1)
			equiv_i = (n - 196) % W + 196
			amounts['se_out'] = len(i_to_state[equiv_i][equiv_u])
			counts['se_out'] = num_outer_diagonals
			print(f"        se_out={amounts['se_out']}x{num_outer_diagonals}")
			
			equiv_u = (-1, 1)
			equiv_i = (n - 196) % H + 196
			amounts['sw_out'] = len(i_to_state[equiv_i][equiv_u])
			counts['sw_out'] = num_outer_diagonals
			print(f"        sw_out={amounts['sw_out']}x{num_outer_diagonals}")
		
		# inner diagonals
		if num_inner_diagonals > 0:
			print(f"	{num_inner_diagonals} inner diagonals per quadrant")
			equiv_u = (-1, -1)
			equiv_i = (n - 327) % W + 327
			amounts['nw_in'] = len(i_to_state[equiv_i][equiv_u])
			counts['nw_in'] = num_inner_diagonals
			print(f"        nw_in={amounts['nw_in']}x{num_inner_diagonals}")
			
			equiv_u = (1, -1)
			equiv_i = (n - 327) % H + 327
			amounts['ne_in'] = len(i_to_state[equiv_i][equiv_u])
			counts['ne_in'] = num_inner_diagonals
			print(f"        ne_in={amounts['ne_in']}x{num_inner_diagonals}")
			
			equiv_u = (1, 1)
			equiv_i = (n - 327) % W + 327
			amounts['se_in'] = len(i_to_state[equiv_i][equiv_u])
			counts['se_in'] = num_inner_diagonals
			print(f"        se_in={amounts['se_in']}x{num_inner_diagonals}")
			
			equiv_u = (-1, 1)
			equiv_i = (n - 327) % H + 327
			amounts['sw_in'] = len(i_to_state[equiv_i][equiv_u])
			counts['sw_in'] = num_inner_diagonals
			print(f"        sw_in={amounts['sw_in']}x{num_inner_diagonals}")
	
	
		# direct inner
		
		if maxu0 >= 2:
			equiv_u = (-1, 0)
			equiv_i = (n - 196) % W + 196
			amounts['w_in'] = len(i_to_state[equiv_i][equiv_u])
			counts['w_in'] = 1
			print(f"        w_in={amounts['w_in']}x1")
			
			equiv_u = (0, -1)
			equiv_i = (n - 196) % W + 196
			amounts['n_in'] = len(i_to_state[equiv_i][equiv_u])
			counts['n_in'] = 1
			print(f"        n_in={amounts['n_in']}x1")
			
			equiv_u = (1, 0)
			equiv_i = (n - 196) % W + 196
			amounts['e_in'] = len(i_to_state[equiv_i][equiv_u])
			counts['e_in'] = 1
			print(f"        e_in={amounts['e_in']}x1")
			
			equiv_u = (0, 1)
			equiv_i = (n - 196) % W + 196
			amounts['s_in'] = len(i_to_state[equiv_i][equiv_u])
			counts['s_in'] = 1
			print(f"        s_in={amounts['s_in']}x1")
		else:
			amounts['centre'] = len(i_to_state[n][(0,0)])
			counts['centre'] = 1
			print(f"        centre={amounts['centre']}x1")


	# inner filled
	
	if maxu0 >= 2:
		if outer_diag:
			parity_outer = maxu0 % 2 + 1
			num_outer = (maxu0 - 1) ** 2
			parity_inner = maxu0 % 2
			num_inner = 0 if maxu0 == 2 else (maxu0 - 2) **2
		else:
			parity_outer = maxu0 % 2
			num_outer = (maxu0 - 2) ** 2
			parity_inner = maxu0 % 2 + 1
			num_inner = 0 if maxu0 == 2 else (maxu0 - 3) **2
			
		if parity_outer == 0:
			equiv_u = (0,0)
			equiv_i = (n - 130) % 2 + 130
		else:
			equiv_u = (-1, 0)
			equiv_i = (n - 261) % 2 + 261
		amounts['filled_outer'] = len(i_to_state[equiv_i][equiv_u])
		counts['filled_outer'] = num_outer
		print(f"        filled_outer={amounts['filled_outer']}x{num_outer}")
		
		
		if parity_inner == 0:
			equiv_u = (0,0)
			equiv_i = (n - 130) % 2 + 130
		else:
			equiv_u = (-1, 0)
			equiv_i = (n - 261) % 2 + 261
		
		amounts['filled_inner'] = len(i_to_state[equiv_i][equiv_u])
		counts['filled_inner'] = num_inner
		print(f"        filled_inner={amounts['filled_inner']}x{num_inner}")
	
	total = 0
	
	for k in amounts:
		total += amounts[k] * counts[k]
	
	return total
	
import traceback
	
for n in N:
	try:
		print(f"steps = {n}, reachable = {calc_reachable(n)}")
	except Exception as e:
		traceback.print_exc()