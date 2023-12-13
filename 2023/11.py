grid = []

while True:
	try:
		line = input()
		grid.append(list(line))
	except EOFError:
		break
		
cols = set()
rows = set()

for r in range(len(grid)):
	for c in range(len(grid[0])):
		if grid[r][c] == '#':
			cols.add(c)
			rows.add(r)
			
expand_cols = sorted(list(set(range(len(grid))) - cols), reverse=True)
expand_rows = sorted(list(set(range(len(grid[0]))) - rows), reverse=True)

print(f"expand cols={expand_cols}")
print(f"expand rows={expand_rows}")

for c in expand_cols:
	for r in range(len(grid)):
		grid[r].insert(c, '.')

for r in expand_rows:
	grid.insert(r, grid[r])

		
print(f"expanded grid:")

for r in grid:
	for c in r:
		print(c, end='')
	print()
	
ps = []

for y in range(len(grid)):
	for x in range(len(grid[0])):
		if grid[y][x] == '#':
			ps.append((x,y))
			
print(f"galaxies = {ps}")
dists = []


for i in range(len(ps)):
	for j in range(i+1, len(ps)):
		p1 = ps[i]
		p2 = ps[j]
		dist = abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])
		dists.append(dist)

print(f"dists={sum(dists)}")


