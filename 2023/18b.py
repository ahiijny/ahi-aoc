instrs = []
nodes = []
edges = []
p = (0.5, 0.5)
nodes.append(p)

dirmap = {
	'0': 'R',
	'1': 'D',
	'2': 'L',
	'3': 'U'
}

while True:
	try:
		i = input().split()
		h = i[2][2:-1]
		distance = int(h[:5], 16)
		direction = dirmap[h[5]]
		instrs.append([direction, distance, i[2][1:-1]])
	except EOFError:
		break
		
print(f"instrs: {instrs}")

deltas = {
	'U': (0, -1),
	'R': (1, 0),
	'D': (0, 1),
	'L': (-1, 0)
}

def add(a, b):
	return (a[0] + b[0], a[1] + b[1])
	
def mul(a, m):
	return(m * a[0], m * a[1])
	
xs = set()
xs.add(p[0])

for instr in instrs:
	face, dist, col = instr
	print(f"> {face} {dist}")
	n2 = add(p, mul(deltas[face], dist))
	nodes.append(n2)
	edges.append([p, n2])
	p = n2
	xs.add(p[0])
	
x_order = sorted(xs)

print(f"unique xs: {x_order}")

if edges[0][0] != edges[-1][-1]:
	print("warning: polygon is not closed")
	
print(f"nodes = {nodes}")
print(f"edges = {edges}")


# edge crosses
# note avoid testing near edges to avoid edge cases
crosses = {}

for e in edges:
	if e[0][0] != e[1][0]: # we only need to worry about vertical edges
		continue
	miny = min(e[0][1], e[1][1])
	maxy = max(e[0][1], e[1][1])
	x = e[0][0]
	if x not in crosses:
		crosses[x] = set()
	crosses[x].add((miny, maxy))
	
def is_cross(x, y):
	if x not in crosses:
		return False
	for miny, maxy in crosses[x]:
		if miny < y and y < maxy:
			return True
	return False

def is_inside(p):
	px = p[0]
	py = p[1]
	crosses = 0
	# ray trace left to right
	for x in x_order:
		if x > px:
			break
		if is_cross(x, py):
			crosses += 1
	result = crosses % 2 == 1
	#print(f"{p} is inside? {result}")
	return result
	
# expand nodes based on shape to include outline
for i, n in enumerate(nodes):
	# test around
	deltas = {
		'nw': (-0.5, -0.5),
		'ne': (0.5, -0.5),
		'se': (0.5, 0.5),
		'sw': (-0.5, 0.5)
	}
	nw = is_inside(add(n, deltas['nw']))
	ne = is_inside(add(n, deltas['ne']))
	se = is_inside(add(n, deltas['se']))
	sw = is_inside(add(n, deltas['sw']))
	
	#print(f"@ {n}: nw={nw}, ne={ne}, se={se}, sw={sw}")
	
	delta = None
	
	if nw and not (ne or se or sw):
		delta = deltas['se']
	elif ne and not (nw or se or sw):
		delta = deltas['sw']
	elif se and not (nw or ne or sw):
		delta = deltas['nw']
	elif sw and not (nw or ne or se):
		delta = deltas['ne']
	elif not nw and (ne and se and sw):
		delta = deltas['nw']
	elif not ne and (nw and se and sw):
		delta = deltas['ne']
	elif not se and (nw and ne and sw):
		delta = deltas['se']
	elif not sw and (nw and ne and se):
		delta = deltas['sw']
	else:
		raise ValueError(f'point at {n} has weird shape!')
	nodes[i] = add(n, delta)
	if i < len(edges):
		edges[i][0] = nodes[i]
	edges[i-1][1] = nodes[i]
	
print(f"expanded nodes: {nodes}")
print(f"expanded edges: {edges}")

# add up signed area of trapezoids
total_area = 0

# https://en.wikipedia.org/wiki/Shoelace_formula

for e in edges:
	# for ccw edges
	# p1 -> p2 negative area if going left to right, positive area if going right to left
	# summing should give area of polygon
	# trapezoid has bottom x1 - x2, h1 = y1, h2 = y2
	# area of trapezoid = 1/2 (a + b) h
	x1 = e[0][0]
	y1 = e[0][1]
	x2 = e[1][0]
	y2 = e[1][1]
	
	area = 0.5 * (y1 + y2) * (x1 - x2)
	total_area += area

print(f"total area: {abs(total_area)}")
