from collections import deque

raw_grid = []
grid = {}

while True:
	try:
		row = input()
		raw_grid.append(list(row))		
	except EOFError:
		break
		
elves = []
		
for y in range(len(raw_grid)):
	for x in range(len(raw_grid[y])):
		if raw_grid[y][x] == '#':
			elves.append([x, y])
			grid[(x,y)] = '#'
			
print(f"elves: {elves}")

def getbounds():
	global grid
	
	minx = min(x for x,y in grid.keys())
	maxx = max(x for x,y in grid.keys())
	miny = min(y for x,y in grid.keys())
	maxy = max(y for x,y in grid.keys())
	return minx, maxx, miny, maxy

def print_grid():
	global grid
	minx, maxx, miny, maxy = getbounds()
	
	for y in range(miny, maxy+1):
		for x in range(minx, maxx+1):
			if (x,y) in grid:
				print('#', end='')
			else:
				print('.', end='')
		print()
		
ROUNDS = 10

order = deque(['n', 's', 'w', 'e'])

print(f"grid: {grid}")

print (f"=== initial state ===")
print_grid()
i = 0

while True:
	print(f"=== round {i+1} ===")
	# propose phase
	propose = {}
	for e in range(len(elves)):
		x, y = elves[e]
		#print(f"elf{e}@{(x,y)}")
		e_n = (x, y-1) in grid
		e_ne = (x+1, y-1) in grid
		e_e = (x+1, y) in grid
		e_se = (x+1, y+1) in grid
		e_s = (x, y+1) in grid
		e_sw = (x-1, y+1) in grid
		e_w = (x-1, y) in grid
		e_nw = (x-1, y-1) in grid
		
		#print(f"...collision check: {[e_n, e_ne, e_e, e_se, e_s, e_sw, e_w, e_nw]}")
		
		if not any([e_n, e_ne, e_e, e_se, e_s, e_sw, e_w, e_nw]):
			continue
		for o in order:
			x2 = None
			y2 = None
			if o == 'n':
				if not e_n and not e_ne and not e_nw:
					#print(" ...propose N")
					x2 = x
					y2 = y - 1
				#else:
					#print("...cannot go N")
			elif o == 's':
				if not e_s and not e_se and not e_sw:
					#print(" ...propose S")
					x2 = x
					y2 = y + 1
				#else:
					#print("...cannot go S")
			elif o == 'w':
				#print(" ...propose W")
				if not e_w and not e_nw and not e_sw:
					x2 = x-1
					y2 = y
				#else:
					#print("...cannot go W")
			elif o == 'e':
				#print(" ...propose E")
				if not e_e and not e_ne and not e_se:
					x2 = x+1
					y2 = y
				#else:
					#print("...cannot go E")
			if x2 is None:
				continue
			if (x2, y2) in propose:
				propose[(x2, y2)].append((e, x, y))
				break
			else:
				propose[(x2, y2)] = [(e, x, y)]
				break
	# move phase
	moved = 0
	for p2, proposers in propose.items():
		#print(f"p2={p2}, proposers={proposers}")
		if len(proposers) > 1:
			continue
		x2 = p2[0]
		y2 = p2[1]
		e = proposers[0][0]
		x = proposers[0][1]
		y = proposers[0][2]
		del grid[(x, y)]
		grid[(x2, y2)] = '#'
		elves[e] = [x2, y2]
		moved += 1
	order.rotate(-1)
	if i < 20:
		print_grid()
	minx, maxx, miny, maxy = getbounds()
	print(f"area={(maxx-minx+1) * (maxy-miny+1) - len(grid)}")
	i += 1
	if moved == 0:
		print(f"no elves moved in round {i}")
		break
