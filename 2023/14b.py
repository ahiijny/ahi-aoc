import copy

grid = []
memo = {}
memo_hists = {}

while True:
	try:
		line = list(input())
		if line:
			grid.append(line)
	except EOFError:
		break
		
# north

def pg():
	for r in grid:
		for c in r:
			print(c, end='')
		print()

directions = ["N", "W", "S", "E"]

def tilt(direction):
	if direction == 'N':
		for x in range(len(grid[0])):
			bot = 0
			for y in range(len(grid)):
				if grid[y][x] == 'O':
					grid[y][x] = '.'
					grid[bot][x] = 'O'
					bot += 1
				elif grid[y][x] == '#':
					bot = y + 1
	elif direction == 'S':
		for x in range(len(grid[0])):
			bot = len(grid)-1
			for y in range(len(grid)-1, -1, -1):
				if grid[y][x] == 'O':
					grid[y][x] = '.'
					grid[bot][x] = 'O'
					bot -= 1
				elif grid[y][x] == '#':
					bot = y - 1
	if direction == 'W':
		for y in range(len(grid)):
			bot = 0
			for x in range(len(grid[0])):
				if grid[y][x] == 'O':
					grid[y][x] = '.'
					grid[y][bot] = 'O'
					bot += 1
				elif grid[y][x] == '#':
					bot = x + 1
	elif direction == 'E':
		for y in range(len(grid)):
			bot = len(grid[0])-1
			for x in range(len(grid[0])-1, -1, -1):
				if grid[y][x] == 'O':
					grid[y][x] = '.'
					grid[y][bot] = 'O'
					bot -= 1
				elif grid[y][x] == '#':
					bot = x - 1
	#print(f"shifted grid -> {direction}:")
	#pg()
	
def get_hash(grid):
	return tuple(tuple(r) for r in grid)

g = get_hash(grid)
memo[g] = 0
memo_hists[0] = g

a = None
b = None

TARGET = 1000000000

for i in range(TARGET):
	tilt('N')
	tilt('W')
	tilt('S')
	tilt('E')
	
	g = get_hash(grid)
	
	if g in memo:
		a = memo[g]
		b = i+1
		print(f"recurrence grid @ {a} <=> {i}")
		break
		
	memo[g] = i+1
	memo_hists[i+1] = g

assert(b < TARGET)
equiv_i = (TARGET - a) % (b - a) + a
equiv_g = memo_hists[equiv_i]
	

total = 0

for y, r in enumerate(equiv_g):
	total += sum(len(equiv_g) - y if equiv_g[y][x] == 'O' else 0 for x in range(len(equiv_g[0])))
	
print(f"total: {total}")
		