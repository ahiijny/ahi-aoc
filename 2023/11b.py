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

def num_warps(p1, p2):
	x1 = min(p1[0], p2[0])
	x2 = max(p1[0], p2[0])
	y1 = min(p1[1], p2[1])
	y2 = max(p1[1], p2[1])
	
	warp_counts = 0
	
	for x in expand_cols:
		if x1 < x and x < x2:
			warp_counts += 1
	for y in expand_rows:
		if y1 < y and y < y2:
			warp_counts += 1
	return warp_counts

ps = []

for y in range(len(grid)):
	for x in range(len(grid[0])):
		if grid[y][x] == '#':
			ps.append((x,y))
			
print(f"galaxies = {ps}")
dists = []

WARP_FACTOR = 1000000

for i in range(len(ps)):
	for j in range(i+1, len(ps)):
		p1 = ps[i]
		p2 = ps[j]
		dist = abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])
		nw = num_warps(p1, p2)
		dist += (WARP_FACTOR - 1) * nw
		dists.append(dist)

print(f"dists={sum(dists)}")


