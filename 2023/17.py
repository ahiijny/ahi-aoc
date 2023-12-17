from collections import deque
import heapq

grid = []
min_dist = {((0,0),()): (0, [(0,0)])} # (point, past_facings): (dist, path)
visited = {}

while True:
	try:
		grid.append([int(x) for x in input()])
	except EOFError:
		break
		
print(f"x y = [{len(grid[0])}, {len(grid)}]")
		
q = [(0, (0,0), [(0,0)])]

dirs = [(1,0), (0, 1), (-1,0), (0,-1)]

def rot(d, amount):
	return dirs[(4 + dirs.index(d) + amount) % 4]

def in_bounds(p):
	return 0 <= p[0] and p[0] < len(grid[0]) and 0 <= p[1] and p[1] < len(grid)

def add(p, d):
	return (p[0] + d[0], p[1] + d[1])

def sub(p1, p2):
	return(p2[0] - p1[0], p2[1] - p1[1])
	
def prev(path):
	prev_facings = []
	for i in range(3):
		b = len(path) - 1 - i
		a = len(path) - 2 - i
		if a < 0:
			break
		f = sub(path[b], path[a])
		if len(prev_facings) == 0:
			prev_facings.append(f)
		elif prev_facings[-1] == f:
			prev_facings.append(f)
		else:
			break
			
	return tuple(prev_facings)


while len(q) > 0:
	dist, p, path = heapq.heappop(q)
	facing = None
	need_change = False
	
	# print(f"visit: dist={dist}, p={p}")
	
	if p == (len(grid)-1, len(grid[0])-1):
		print(f"path={path}")
		print(f"arrived at destination with heat loss={dist}")
		
		if False:
			for y in range(len(grid)):
				for x in range(len(grid[0])):
					if (x,y) in path:
						print('.', end='')
					else:
						print(grid[y][x], end='')
				print()
		break
	
	
	if len(path) >= 2:
		facing = sub(path[-2], path[-1])
	if len(path) >= 3:
		facing2 = sub(path[-3], path[-2])
	if len(path) >= 4:
		facing3 = sub(path[-4], path[-3])
		if facing == facing2 and facing2 == facing3:
			need_change = True
			
	past_facings = prev(path)
	
	if (p, past_facings) in visited:
			continue
			
	for d in dirs:
		p2 = add(p, d)
		if not in_bounds(p2):
			continue
		if facing is not None and rot(d, 2) == facing:
			continue
		if need_change and d == facing:
			continue
		dist2 = dist + grid[p2[1]][p2[0]]
		path2 = list(path) + [p2]
		pf2 = prev(path2)
		if (p2, pf2) in visited:
			continue
		if (p2, pf2) not in min_dist:
			min_dist[(p2, pf2)] = (dist2, path2)
			heapq.heappush(q, (dist2, p2, path2))
		else:
			prev_d2 = min_dist[(p2, pf2)][0]
			if prev_d2 > dist2:
				min_dist[(p2, pf2)] = (dist2, path2)
				heapq.heappush(q, (dist2, p2, path2))
	visited[(p, past_facings)] = True
