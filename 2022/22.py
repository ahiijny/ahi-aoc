from collections import deque

grid = []
steps = []
facing = [
	[1, 0],
	[0, 1],
	[-1, 0],
	[0, -1]
]

max_width = 0


while True:
	line = input()
	#print(f"line={line}")
	if "." not in line:
		break
	grid.append(list(line))
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


print(f"grid: {grid}")
print(f"instructions: {steps}")

y = 0
x = 0

# find begin
while grid[y][x] != '.':
	x += 1

start = [y, x]
face_idx = 0

def advance(grid, x, y, face, amount):
	assert grid[y][x] == '.'
	remaining = amount
	
	while remaining > 0:
		x2 = (x + face[0]) % len(grid[0])
		y2 = (y + face[1]) % len(grid)
		if grid[y2][x2] == '#':
			remaining = 0
		elif grid[y2][x2] == ' ':
			# warp:
			while grid[y2][x2] == ' ':
				x2 = (x2 + face[0]) % len(grid[0])
				y2 = (y2 + face[1]) % len(grid)
		if grid[y2][x2] == '.':
			remaining -= 1
			x = x2
			y = y2
		else:
			remaining = 0
	return x, y
	
print(f"start at: y={y},x={x}")
	
for i, step in enumerate(steps):
	if type(step) == int:
		print(f"[{step}] ({x},{y}): facing={face_idx}, amount={step}")
		x, y = advance(grid, x, y, facing[face_idx], step)
	else:
		if step == 'R':
			face_idx = (face_idx + 1) % len(facing)
		elif step == 'L':
			face_idx = (face_idx - 1) % len(facing)
		else:
			raise ValueError(f"step????? {step}")
		print(f"[{step}] ({x},{y}): facing={face_idx}")
			
print(f"final location: x={x}, y={y}, facing={face_idx}")
print(f"password={1000*(y+1) + 4*(x+1) + face_idx}")

			
		
	
	
