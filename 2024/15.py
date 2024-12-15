def bounds(x, y):
	return 0 <= x and x < len(grid[0]) and 0 <= y and y < len(grid)
	
def add(p1, p2):
	return (p1[0] + p2[0], p1[1] + p2[1])
	
def mul(p, s):
	return (p[0] * s, p[1] * s)
	
grid = []
moves = []
dirs = {
	'<': (-1, 0),
	'^': (0, -1),
	'>': (1, 0),
	'v': (0,1)
}
robot = None
boxes = []

try:
	while True:
		line = input()
		if line == "":
			break
		grid.append([c for c in line])
	while True:
		line = input()
		moves.extend([m for m in line])
except EOFError:
	pass

H = len(grid)
W = len(grid[0])
	
def print_grid():
	for y in range(H):
		for x in range(W):
			print(grid[y][x], end='')
		print()
	
print_grid()
print(moves)
print(dirs)

for y in range(H):
	for x in range(W):
		if grid[y][x] == '@':
			robot = (x,y)
		elif grid[y][x] == 'O':
			boxes.append((x,y))
			
print(f"robot: {robot}")
print(f"boxes: {boxes}")

def try_move(p, d, cur='@'):
	deltas = {}
	p2 = add(p, d)
	x = p2[0]
	y = p2[1]
	if grid[y][x] == '#':
		return deltas
	elif grid[y][x] == '.':
		deltas[p] = '.'
		deltas[p2] = cur
		return deltas
	elif grid[y][x] == 'O':
		d2 = try_move(p2, d, 'O')
		if len(d2) == 0:
			return d2
		for k,v in d2.items():
			deltas[k] = v
		deltas[p] = '.'
		deltas[p2] = cur
		return deltas
	else:
		raise ValueError("shouldn't happen")

for i, m in enumerate(moves):
	print(f"move {i}: {m}")
	p = robot
	d = dirs[m]
	deltas = try_move(p, d)
	for p,v in deltas.items():
		grid[p[1]][p[0]] = v
		if v == '@':
			robot = p
	#print_grid()
print_grid()
total = 0
	
for y in range(H):
	for x in range(W):
		if grid[y][x] == 'O':
			total += x + 100 * y
print(total)
			
