grid = []

try:
	while True:
		line = input()
		grid.append(line)
except EOFError:
	pass

locs = {}
antinodes = {}
allnodes = set()

for y in range(len(grid)):
	for x in range(len(grid[0])):
		c = grid[y][x]
		if c != '.':
			if c not in locs:
				locs[c] = [(x,y)]
			else:
				locs[c].append((x,y))
	
def valid(p):
	return 0 <= p[0] < len(grid[0]) and 0 <= p[1] < len(grid)
	
def sub(a, b):
	return (a[0] - b[0], a[1] - b[1])

def add(a, b):
	return (a[0] + b[0], a[1] + b[1])				

total = 0

for key, value in locs.items():
	antis = set()
	for i in range(len(value)):
		for j in range(i+1, len(value)):
			a = value[i]
			b = value[j]
			#  a --- b
			# b - a = vector pointing from a to b
			d1 = sub(b, a)
			anode1 = add(b, d1)
			d2 = sub(a, b)
			anode2 = add(a, d2)
			
			if valid(anode1):
				antis.add(anode1)
			if valid(anode2):
				antis.add(anode2)
	antinodes[key] = antis
	allnodes.update(antis)
	
for y in range(len(grid)):
	for x in range(len(grid[0])):
		anti = []		
		for k, v in antinodes.items():
			if (x,y) in v:
				anti.append(k)
				break
		if len(anti) == 0:
			if grid[y][x] != '.':
				print('x', end='')
			else:
				print('.', end='')
		elif len(anti) == 1:
			print(anti[0], end='')
		else:
			print(len(anti), end='')
	print()

print(f"{len(grid[0])}x{len(grid)}")
print(total)
print(len(allnodes))


			
