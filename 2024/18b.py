import heapq

H = W = 71
n = 1024

dirs = [
	(-1, 0),
	(0, -1),
	(1, 0),
	(0,1)
]
	
grid = []
start = (0,0)
end = (W-1,H-1)
blocks = []

def bounds(x, y):
	return 0 <= x and x < len(grid[0]) and 0 <= y and y < len(grid)
	
def add(p1, p2):
	return (p1[0] + p2[0], p1[1] + p2[1])
	
def mul(p, s):
	return (p[0] * s, p[1] * s)
	
try:
	while True:
		blocks.append(tuple(int(a) for a in input().split(",")))
except EOFError:
	pass

grid = [['.' for x in range(W)] for y in range(H)]

def can_reach_exit():
	visited = {}
	q = [start]
	while len(q) > 0:
		p = q.pop()
		if p in visited:
			continue
		visited[p] = True
		for d in dirs:
			p2 = add(p, d)
			if bounds(*p2) and grid[p2[1]][p2[0]] != '#':
				q.append(p2)
				visited[p] = True
	return end in visited

def print_grid():
	for y in range(H):
		for x in range(W):
			print(grid[y][x], end='')
		print()

for i, b in enumerate(blocks):
	print(f"checking i={i}")
	grid[b[1]][b[0]] = '#'
	if i >= n:
		if not can_reach_exit():
			print_grid()
			print(f"exit unreachable on block i={i}, b={b}")
			break
		
