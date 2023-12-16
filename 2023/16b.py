from collections import deque

grid = []

while True:
	try:
		grid.append(list(input()))
	except EOFError:
		break



dirs = [(1,0), (0, 1), (-1,0), (0,-1)]

def rot(d, amount):
	return dirs[(4 + dirs.index(d) + amount) % 4]

def in_bounds(p):
	return 0 <= p[0] and p[0] < len(grid[0]) and 0 <= p[1] and p[1] < len(grid)

def add(p, d):
	return (p[0] + d[0], p[1] + d[1])

def beam(start, start_dir):
	on = {}
	seen = {}

	q = deque()
	q.append((start, start_dir))

	while len(q) > 0:
		p, d = q.popleft()
		seen[(p,d)] = True
		on[p] = True
		
		c = grid[p[1]][p[0]]
		if c == '.' or (abs(d[0]) == 1 and c == '-') or (abs(d[1]) == 1 and c == '|'):
			dn = [d]
		elif (abs(d[0]) == 0 and c == '-') or (abs(d[1]) == 0 and c == '|'):
			# split
			dn = [rot(d, 1), rot(d, -1)]
		elif c == '/':
			if d == (0, 1) or d == (0, -1):
				dn = [rot(d, 1)]
			else:
				dn = [rot(d, -1)]
		elif c == '\\':
			if d == (0, 1) or d == (0, -1):
				dn = [rot(d, -1)]
			else:
				dn = [rot(d, 1)]
		
		for n in dn:
			p2 = add(p, n)
			if in_bounds(p2) and (p2, n) not in seen:
				q.append((p2, n))
				seen[(p2,n)] = True
				on[p2] = True
	print(f"start = {start}, num on={len(on)}")
	return len(on)
		
if False:
	for y, r in enumerate(grid):
		for x, c in enumerate(r):
			if (x,y) in on:
				print('#', end='')
			else:
				print('.', end='')
		print()

ons = []
		
for y in range(len(grid)):
	ons.append(beam((0, y), (1,0)))
	ons.append(beam((len(grid[0])-1, y), (0,1)))

for x in range(len(grid[0])):
	ons.append(beam((x, 0), (0,1)))
	ons.append(beam((x, len(grid)-1), (0,-1)))
	
print(max(ons))
			

	
		
	
	