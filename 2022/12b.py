from collections import deque
from operator import add, sub

def val(ch):
	if ch == 'S':
		return val('a')
	elif ch == 'E':
		return val('z')
	return ord(ch) - ord('a')
	
	
start = None
end = None
orig = []
grid = []

def pgrid(grid):
	for r in grid:
		print('\t'.join([str(c) for c in r]))

while True:
	try:
		line = input()
		orig.append(line)
		grid.append(list(val(ch) for ch in line))
	except EOFError:
		break
		
for r, row in enumerate(orig):
	for c, cell in enumerate(row):
		if cell == 'S':
			start = (r, c)
		elif cell == 'E':
			end = (r, c)
		
visited = [[False for c in r] for r in grid]
			
q = deque()
q.append((end, []))

deltas = [
	[1, 0],
	[0, 1],
	[0, -1],
	[-1, 0]
]

print(f"start: {start}, end = {end}")
pgrid(grid)
print(visited)

finis = False

c = 0

# reverse

while len(q) > 0 and not finis:
	loc, path = q.popleft()
	# print(f"loc = {loc}, path = {path}")
	visited[loc[0]][loc[1]] = True
	c += 1
	if c % 100 == 0:
		print(f"progress: {loc}, {len(path)}")
	
	for d in deltas:
		n = (loc[0] + d[0], loc[1] + d[1])
		if 0 <= n[0] and n[0] < len(grid) and 0 <= n[1] and n[1] < len(grid[0]):
			h = grid[loc[0]][loc[1]]
			h2 = grid[n[0]][n[1]]
			path2 = list(path)
			path2.append(n)
			if h2 >= h - 1:
				# ok
				if grid[n[0]][n[1]] == 0:
					print(f"found end: path = {path2}, len = {len(path2)}")
					finis = True
				if not visited[n[0]][n[1]]:
					q.append((n, path2))
					visited[n[0]][n[1]] = True

