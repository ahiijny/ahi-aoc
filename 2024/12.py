grid = []

try:
	while True:
		grid.append(input())
except EOFError:
	pass
	
print(grid)

p = {}
a = {}
	
region = {}	
ri = 0

def bounds(x, y):
	return 0 <= x and x < len(grid[0]) and 0 <= y and y < len(grid)
	
def add(p1, p2):
	return (p1[0] + p2[0], p1[1] + p2[1])

ds = [
	(1, 0),
	(0, 1),
	(-1, 0),
	(0, -1)	
]

# explore regions
for y in range(len(grid)):
	for x in range(len(grid[0])):
		if (x,y) in region:
			continue
		q = []
		region[(x,y)] = ri
		cur = grid[y][x]
		q.append((x,y))
		while len(q) > 0:
			v = q.pop()
			for d in ds:
				v2 = add(v, d)
				if bounds(*v2) and v2 not in region and grid[v2[1]][v2[0]] == cur:
					region[v2] = ri
					q.append(v2)
		ri += 1
		
for y in range(len(grid)):
	for x in range(len(grid[0])):
		print(region[(x,y)], end=' ')
	print()
	
for y in range(len(grid)):
	for x in range(len(grid[0])):
		ri = region[(x,y)]
		k = (ri, grid[y][x])
		if k not in p:
			p[k] = 0
		if k not in a:
			a[k] = 0

	
# horizontal
# include area count

def get(x, y):
	if 0 <= x and x < len(grid[0]) and 0 <= y and y < len(grid):
		return grid[y][x]
	return None

for y in range(len(grid)):
	cur = None
	ri = None
	for x in range(len(grid[0])+ 1):
		if get(x,y) != cur:
			# close prev
			if cur is not None:
				p[(ri, cur)] += 1
			cur = get(x,y)
			ri = region[(x,y)] if (x,y) in region else None
			if cur is not None:
				p[(ri, cur)] += 1
		ri = region[(x,y)] if (x,y) in region else None
		if cur is not None:
			a[(ri, cur)] += 1	

# vertical

for x in range(len(grid[0])):
	cur = None
	ri = None
	for y in range(len(grid)+1):
		if get(x,y) != cur:
			# close prev
			if cur is not None:
				p[(ri, cur)] +=1
			cur = get(x,y)
			ri = region[(x,y)] if (x,y) in region else None
			if cur is not None:
				p[(ri, cur)] += 1
				
# calc

total = 0

for k in p:
	ri, cur = k
	pk = p[k]
	ak = a[k]
	print(f"{k}: p={pk}, a={ak}")
	total += pk * ak
	
print(f"total: {total}")
