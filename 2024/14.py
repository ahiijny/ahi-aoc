import math

grid = []
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

N = 100
counts = {}
for i in range(-1, 4):
	counts[i] = 0

for i, r in enumerate(robots):
	p = r[0]
	v = r[1]
	p2 = add(p, mul(v, N))
	p2 = coords(*p2)
	print(p2)
	q = quad(*p2)
	counts[q] += 1
	
print(counts)

safety = math.prod(counts[i] for i in range(4))
print(safety)
	