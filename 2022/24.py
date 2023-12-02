from collections import deque

raw_grid = []
grid = {}
blizzards = []

dirs = {
	'>': [1, 0],
	'v': [0, 1],
	'<': [-1, 0],
	'^': [0, -1],
}

while True:
	try:
		row = input()
		raw_grid.append(list(row))		
	except EOFError:
		break

W = len(raw_grid[0])
H = len(raw_grid)	
	
for y in range(len(raw_grid)):
	for x in range(len(raw_grid[y])):
		if raw_grid[y][x] == '#':
			grid[(x,y)] = '#'
		elif raw_grid[y][x] in dirs:
			blizzards.append((x,y, raw_grid[y][x]))
			if (x,y) in grid:
				grid[(x,y)].add(len(blizzards)-1)
			else:
				grid[(x,y)] = set([len(blizzards)-1])
			
			
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
				if type(grid[(x,y)]) != set:
					print(grid[(x,y)], end='')
				elif len(grid[(x,y)]) == 1:
					print(blizzards[next(iter(grid[(x,y)]))][2], end='')
				else:
					print('2', end='')
			else:
				print('.', end='')
		print()
		
print_grid()
print(f"blizzards: {blizzards}")

probes = []
x = 0
y = 0
while (x, y) in grid:
	x += 1
	
print(f"starting at (x,y) = {(x,y)}")
survivors = {(x,y): [(x,y)]}

x = 0
y = H-1
while (x, y) in grid:
	x += 1
	
exit_x = x
exit_y = y
print(f"target exit at (x,y) = {(x,y)}")

t = 0

survivor_path = None

while survivor_path == None:
	# calculate nexts
	all_nexts = {}
	for (x,y), p in survivors.items():
		nexts = [
			(x, y),
			(x+1, y),
			(x, y+1),
			(x-1, y),
			(x, y-1)
		]
		for n in nexts:
			if n in grid and grid[n] == '#':
				continue
			if n in all_nexts:
				continue
			if y < 0 or y >= H:
				continue
			all_nexts[n] = p + [n]
	print(f'number of potential next moves: {len(all_nexts)}')
	# print(f'next moves: {all_nexts}')
	
	# calculate blizzards	
	for i, b in enumerate(blizzards):
		x, y, facing = b
		offset = dirs[facing]
		x2 = (x + offset[0]) % W
		y2 = (y + offset[1]) % H
		while (x2, y2) in grid and grid[(x2,y2)] == '#': # warp
			x2 = (x2 + offset[0]) % W
			y2 = (y2 + offset[1]) % H
		blizzards[i] = (x2, y2, facing)
		grid[(x,y)].remove(i)
		if len(grid[(x,y)]) == 0:
			del grid[(x, y)]
		if (x2, y2) in grid:
			grid[(x2, y2)].add(i)
		else:
			grid[(x2, y2)] = set([i])
	t += 1
	print(f"t={t}")
	# print_grid()
	
	# prune collisions
	survivors = {}
	for n, path in all_nexts.items():
		if n not in grid:
			survivors[n] = path
		if n == (exit_x, exit_y):
			print(f"surviving path to exit found")
			survivor_path = path
	print(f"num survivors={len(survivors)}")
		
print(f"survivor path: minutes={len(survivor_path)-1}: {survivor_path}")
		