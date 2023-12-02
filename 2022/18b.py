from collections import deque

grid = {}
visited = {}

while True:
	try:
		vox = tuple(int(d) for d in input().split(','))
		grid[vox] = True
	except EOFError:
		break

# count surface area

print(f"voxels: {grid}")

minx = min(v[0] for v in grid.keys())
maxx = max(v[0] for v in grid.keys())
miny = min(v[1] for v in grid.keys())
maxy = max(v[1] for v in grid.keys())
minz = min(v[2] for v in grid.keys())
maxz = max(v[2] for v in grid.keys())
print(f"bounds: [{minx}..{maxx}, {miny}..{maxy}, {minz}..{maxz}]")

q = deque()
q.append((minx-1, miny-1, minz-1))

count = 0

while len(q) > 0:
	x, y, z = q.popleft()
	count += 1
	if count % 100 == 0:
		print(f"checking {count} nodes, total reachable={len(visited)}")
		
	visited[(x, y, z)] = True
	todo = [
		(x-1, y, z),
	    (x+1, y, z),
	    (x, y-1, z),
        (x, y+1, z),
        (x, y, z-1),
        (x, y, z+1),
	]
	
	for p2 in todo:
		x2, y2, z2 = p2
		if x2 < minx-1 or x2 > maxx + 1 or y2 < miny-1 or y2 > maxy + 1 or z2 < minz-1 or z2 > maxz+1:
			continue
		if (x2, y2, z2) in visited:
			continue
		if (x2, y2, z2) in grid:
			continue
		q.appendleft((x2, y2, z2))
		visited[(x2, y2, z2)] = True
		
total_area = 0

for x, y, z in grid.keys():
	sides = 6
	todo = [
		(x-1, y, z),
	    (x+1, y, z),
	    (x, y-1, z),
        (x, y+1, z),
        (x, y, z-1),
        (x, y, z+1),
	]
	for p in todo:
		if p in grid or p not in visited:
			sides -= 1
	
	total_area += sides
	
print(f"total area: {total_area}")