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
			p[k] = set()
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
				p[(ri, cur)].add(((x,y),(x,y+1)))
			cur = get(x,y)
			ri = region[(x,y)] if (x,y) in region else None
			if cur is not None:
				p[(ri, cur)].add(((x,y),(x,y+1)))
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
				p[(ri, cur)].add(((x,y),(x+1,y)))
			cur = get(x,y)
			ri = region[(x,y)] if (x,y) in region else None
			if cur is not None:
				p[(ri, cur)].add(((x,y),(x+1,y)))
				
# calculate number of straight edges per area

print(p)

# walk edges

pe_count = {}

for k, edges in p.items():
	ri, cur = k
	edge_groups = {}
	ei = 0
	for e in edges:
		if e in edge_groups:
			continue
		q = []
		q.append(e)
		while len(q) > 0:
			e_cur = q.pop()
			if e_cur in edge_groups:
				continue
			edge_groups[e_cur] = ei
			p1, p2 = e_cur
			x1, y1 = p1
			x2, y2 = p2
			ds = []
			cs = [] # cross check, only need to check 1, lets check right
			if x1 == x2:
				ds = [(0, 1), (0, -1)]
				cs = [(1, 0), (1, 0)]
			elif y1 == y2:
				ds = [(1, 0), (-1, 0)]
				cs = [(0, 1), (0, 1)]
			else:
				raise ValueError("shouldn't happen")
			for d, c in zip(ds, cs):
				q1 = add(p1, d)
				q2 = add(p2, d)
				
				# 4 cases:
				#                 x
				# moving right p1-p2=q2
				#                 ?                
				#
				#                 x
				# moving left  q1=p1-p2
				#                 ?
				#
				# moving down  p1
				#			   |
				#			 x p2 ?
				#              ||
				#			   q2
				#
				# moving up    q1
				#			   ||
				#			 x p1 ?
				#              |
				#			   q2
				
				c1 = None
				if d[0] == 1 or d[1] == 1:
					c1 = p2
				elif d[0] == -1 or d[1] == -1:
					c1 = p1
				else:
					raise ValueError("shouldn't happen")
				c2 = add(c1, c)
				if (q1, q2) in edges:
					# additional constraint: if it is a + type fence, it does not connect across the corner
					# |- type is not possible bc otherwise the inner would be joined
					# so only need to check one across
					if (c1, c2) not in edges:
						q.append((q1, q2))
		ei += 1
		pe_count[k] = ei
	print(f"k={k}, edge_groups={edge_groups}")

print(f"side count per group: {pe_count}")
			
				
# calc

total = 0

for k in a:
	ri, cur = k
	ak = a[k]
	pk = pe_count[k]
	print(f"{k}: a={ak}, p={pk}")
	total += pk * ak

print(f"total: {total}")
