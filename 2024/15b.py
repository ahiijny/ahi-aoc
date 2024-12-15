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
		grid.append([c for c in line.replace(".", "..").replace("#", "##").replace("O", "[]").replace("@", "@.")])
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

def is_shiftable(ps, d):
	# scan column ahead
	#
	#
	#    #
	# []  []
	#  [][]
	#   []
	#    @		
	all_free = True
	p2s = set()
	for p in ps:
		p2 = add(p, d)
		c = grid[p2[1]][p2[0]]
		if c != '.':
			all_free = False
		if c == '#':
			return False
		elif c == '[' or c == ']':
			p2s.add(p2)
		if d[1] != 0:
			if c == '[':
				p2s.add((p2[0]+1, p2[1]))
			elif c == ']':
				p2s.add((p2[0]-1, p2[1]))
	if all_free:
		return True
	return is_shiftable(p2s, d)

def move(ps, d):
	p2s = set()
	all_free = True
	#print(f"move: ps={ps}, d={d}")
	for p in ps:
		p2 = add(p, d)
		c = grid[p2[1]][p2[0]]
		if c != '.':
			all_free = False
			p2s.add(p2)
		if d[1] != 0:
			if c == '[':
				p2s.add((p2[0]+1, p2[1]))
			elif c == ']':
				p2s.add((p2[0]-1, p2[1]))
	if not all_free:
		move(p2s, d)
	for p in ps:
		p2 = add(p, d)
		c = grid[p[1]][p[0]]
		#print(f"  m:{c} : {p} -> {p2}")
		grid[p2[1]][p2[0]] = c
		grid[p[1]][p[0]] = '.'
				

for i, m in enumerate(moves):
	#print(f"move {i}: {m}")
	p = robot
	d = dirs[m]
	if not is_shiftable([p], d):
		continue
	move([p], d)
	robot = add(robot, d)
	#print_grid()
print_grid()
total = 0
	
for y in range(H):
	for x in range(W):
		if grid[y][x] == '[':
			total += x + 100 * y
print(total)
			
