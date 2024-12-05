grid = []
used = []

try:
	while True:
		line = input()
		grid.append(line)
except EOFError:
	pass

H = len(grid)
W = len(grid[0])

used = [[False for x in range(W)] for y in range(H)]
	
def loc(p):
	x = p[0]
	y = p[1]
	if 0 <= x and x < W and 0 <= y and y < H:
		return (x, y)
	raise ValueError()
	
word = 'XMAS'
vectors = [
	(1, 0),
	(1, 1),
	(0, 1),
	(-1, 1),
	(-1, 0),
	(-1, -1),
	(0, -1),
	(1, -1)
]

def add(p, v):
	return (p[0] + v[0], p[1] + v[1])

print(grid)
print(loc((1, 1)))

matches = 0

for y in range(H):
	for x in range(W):
		for v in vectors:
			try:
				match = True
				p = (x, y)
				use = [p]
				for i in range(len(word)):
					if i != 0:
						p = loc(add(p, v))
					if grid[p[1]][p[0]] != word[i]:
						match = False
						break
					use.append(p)
				if match:
					matches += 1
					for r in use:
						used[r[1]][r[0]] = True
			except ValueError:
				continue
				
def print_used():
	for y in range(H):
		for x in range(W):
			if used[y][x]:
				print(grid[y][x], end='')
			else:
				print('.', end='')
		print()
		
print_used()

print(matches)