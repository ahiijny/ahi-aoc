grid = []

while True:
	try:
		line = list(input())
		if line:
			grid.append(line)
	except EOFError:
		break
		
# north

for x in range(len(grid[0])):
	bot = 0
	for y in range(len(grid)):
		if grid[y][x] == 'O':
			grid[y][x] = '.'
			grid[bot][x] = 'O'
			bot += 1
		elif grid[y][x] == '#':
			bot = y + 1
			
print(f"shifted grid:")

for r in grid:
	for c in r:
		print(c, end='')
	print()

total = 0

for y, r in enumerate(grid):
	total += sum(len(grid) - y if grid[y][x] == 'O' else 0 for x in range(len(grid[0])))
	
print(f"total: {total}")
		