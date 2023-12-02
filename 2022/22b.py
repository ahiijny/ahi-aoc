from collections import deque
import math

grid = []
steps = []
facing = [
	[1, 0],
	[0, 1],
	[-1, 0],
	[0, -1]
]

max_width = 0
area = 0
W = None

while True:
	line = input()
	#print(f"line={line}")
	if "." not in line:
		break
	grid.append(list(line))
	area += len(line.replace(' ', ''))
	max_width = max(max_width, len(line))
	
# extend

for y in range(len(grid)):
	if len(grid[y]) < max_width:
		grid[y].extend([' '] * (max_width - len(grid[y])))

instr = input()
#print(f"instr={instr}")
left = 0
right = 0
isint = True

# calculate cube warps

print(f"net height = {len(grid)}, net width = {max_width}, area = {area}")
W = int(round(math.sqrt(area / 6)))
print(f"unit square = {W}")

# find cube locations
face_starts = []
for y in range(0, len(grid), W):
	for x in range(0, max_width, W):
		if grid[y][x] != ' ':
			face_starts.append((x, y))
			
print(f"face locations: {face_starts}")

# read in warps

warp_faces = {} # (area, direction) -> (area, rotations)
input()

while True:
	try:
		data = input()
		if data.strip() == "":
			break
		data = data.split()
		area1 = int(data[0])
		dir1 = int(data[1])
		area2 = int(data[2])
		rot = int(data[3])
		warp_faces[(area1, dir1)] = (area2, rot)
		
		# calculate the inverse as well
		dir2_inv = ((dir1 + rot)+2) % 4
		rot_inv = -1 * rot
		warp_faces[(area2, dir2_inv)] = (area1, rot_inv)
	except EOFError:
		break
		
print(f"recorded warps={len(warp_faces)}: (area #, direction) -> (area #, rotations): {warp_faces}")

def get_edge_points(area_start, dir_idx, out=True):
	# we are given the top left corner
	# iteration of points is 1 CW turn from direction vector
	global grid
	global W
	start = None
	transverse = facing[(dir_idx+1)%4]
	
	if out:
		starts = [
			(area_start[0]+W-1, area_start[1]), # right
			(area_start[0]+W-1, area_start[1]+W-1), # down
			(area_start[0], area_start[1]+W-1), #left
			(area_start[0], area_start[1]) # up
		]
	else:
		starts = [
			(area_start[0], area_start[1]), # right
			(area_start[0]+W-1, area_start[1]), # down
			(area_start[0]+W-1, area_start[1]+W-1), #left
			(area_start[0], area_start[1]+W-1) # up
		]
	start = starts[dir_idx]
	p = list(start)
	for i in range(W):
		if grid[p[1]][p[0]] == ' ':
			raise ValueError(f"Error in edge warp calculation: area_start={area_start}, dir_idx={dir_idx}, transverse={transverse}, point#={i}, coords p={p} not in grid")
		yield p
		p[0] += transverse[0]
		p[1] += transverse[1]
		
warps = {} # map from (facing_idx, x, y) to (facing_idx2, x2, y2)

# calc warp coordinates
for k, v in warp_faces.items():
	a1 = k[0]
	d1 = k[1]
	a2 = v[0]
	rot = v[1]
	d2 = (d1 + rot) % 4
	print(f"calculating point warps for area{a1}@{face_starts[a1]} dir={d1} to area{a2}@{face_starts[a2]} dir={d2}")
	for (x1, y1), (x2, y2) in zip(get_edge_points(face_starts[a1], d1, out=True), get_edge_points(face_starts[a2],d2,out=False)):
		assert(d1, x1, y1) not in warps
		print(f"{d1}{(x1, y1)} -> {d2}{(x2, y2)}")
		warps[(d1, x1, y1)] = (d2, x2, y2)
		
def print_warps():
	global grid
	global warps
	
	for y in range(len(grid)):
		for x in range(len(grid[0])):
			ch = grid[y][x]
			for i in range(4):
				if (i, x, y) in warps:
					ch = 'W'
			print(ch, end='')
		print()

def print_path(path):
	global grid
	
	for y in range(len(grid)):
		for x in range(len(grid[0])):
			ch = grid[y][x]
			if (x, y) in path:
				ch = path[(x,y)]
			print(ch, end='')
		print()


print(f"===WARPS:===")
print_warps()

# read instructions

while left < len(instr):
	if isint:
		if right < len(instr) and instr[right].isnumeric():
			right += 1
		else:
			steps.append(int(instr[left:right]))
			left = right
			right = left + 1
			isint = False
	else:
		if right < len(instr) and not instr[right].isnumeric():
			right += 1
		else:
			steps.append(instr[left:right])
			isint = True
			left = right
			right = left + 1

print(f"instructions: {steps}")

y = 0
x = 0

# find begin
while grid[y][x] != '.':
	x += 1

start = [y, x]
face_idx = 0
path = {}
path_draw = [
	'>',
	'v',
	'<',
	'^'
]

def advance(grid, x, y, face_idx, amount):
	# print(f"@{(x,y)}, facing={face_idx}, advance={amount}")
	global warps
	global path
	
	assert grid[y][x] == '.'
	remaining = amount
	face = facing[face_idx]
	
	while remaining > 0:
		x2 = x + face[0]
		y2 = y + face[1]
		face_idx2 = face_idx
		face2 = face
		if x2 < 0 or x2 >= len(grid[0]) or y2 < 0 or y2 >= len(grid) or grid[y2][x2] == ' ': # hit boundary
			# warp
			if (face_idx, x, y) in warps:
				warpy = warps[(face_idx, x, y)]
				print(f"following warp{(face_idx, x, y)} to {warpy}")
				face_idx2 = warpy[0]
				face2 = facing[face_idx2]
				x2 = warpy[1]
				y2 = warpy[2]
			else:
				raise ValueError(f"this is a CUBE so this shouldn't happen... missing warp for facing, x, y = {(face_idx, x, y)}")
		elif grid[y2][x2] == '#':
			remaining = 0
		if grid[y2][x2] == '.':
			remaining -= 1
			x = x2
			y = y2
			face_idx = face_idx2
			face = face2
			path[(x,y)] = path_draw[face_idx]
		else:
			remaining = 0
	return x, y, face_idx
	
print(f"start at: y={y},x={x}")
	
for i, step in enumerate(steps):
	if type(step) == int:
		print(f"[{step}] ({x},{y}): facing={face_idx}, amount={step}")
		x, y, face_idx = advance(grid, x, y, face_idx, step)
	else:
		if step == 'R':
			face_idx = (face_idx + 1) % len(facing)
		elif step == 'L':
			face_idx = (face_idx - 1) % len(facing)
		else:
			raise ValueError(f"step????? {step}")
		print(f"[{step}] ({x},{y}): facing={face_idx}")

print_path(path)

print(f"final location: x={x}, y={y}, facing={face_idx}")
print(f"password={1000*(y+1) + 4*(x+1) + face_idx}")
