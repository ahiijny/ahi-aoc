import math

#W = 11
W = 101
#H = 7
H = 103

robots = []

def bounds(x, y):
	return 0 <= x and x < len(grid[0]) and 0 <= y and y < len(grid)
	
def add(p1, p2):
	return (p1[0] + p2[0], p1[1] + p2[1])
	
def mul(p, s):
	return (p[0] * s, p[1] * s)
	
def coords(x, y):
	x = (x + W) % W
	y = (y + H) % H
	return (x, y)
	
def quad(x, y):
	if x == W // 2 or y == H // 2:
		return -1
	elif x < W // 2 and y < H // 2:
		return 0
	elif x > W // 2 and y < H // 2:
		return 1
	elif x < W // 2 and y > H // 2:
		return 2
	elif x > W // 2 and y > H // 2:
		return 3
	raise ValueError("invalid")


try:
	while True:
		line = input().split()
		p = tuple(int(a) for a in line[0][2:].split(","))
		v = tuple(int(a) for a in line[1][2:].split(","))
		robots.append((p,v))		
except EOFError:
	pass
	
print(robots)

N = 10000
counts = {}
for i in range(-1, 4):
	counts[i] = 0

def print_grid(grid):
	for y in range(H):
		for x in range(W):
			if (x,y) in grid:
				print(grid[(x,y)],end='')
			else:
				print('.', end='')
		print()
			

for t in range(N):
	print(f"t={t+1}")
	grid = {}
	for i, r in enumerate(robots):
		p = r[0]
		v = r[1]
		p2 = add(p, v)
		p2 = coords(*p2)
		robots[i] = (p2, v)
		if p2 not in grid:
			grid[p2] = 1
		else:
			grid[p2] += 1
	all_ones = True
	for k,v in grid.items():
		if v != 1:
			all_ones = False
			break
	if all_ones:
		print_grid(grid)
	
print(counts)

safety = math.prod(counts[i] for i in range(4))
print(safety)



	