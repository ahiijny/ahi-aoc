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
	for i in range(10):
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

def streak(path):
	prev_facings = []
	for i in range(len(path)-1):
		b = len(path) - 1 - i
		a = len(path) - 2 - i
		f = sub(path[b], path[a])
		if len(prev_facings) == 0:
			prev_facings.append(f)
		elif prev_facings[-1] == f:
			prev_facings.append(f)
		else:
			break
	return len(prev_facings)

while len(q) > 0:
	dist, p, path = heapq.heappop(q)
	facing = None
	
	#print(f"visit: dist={dist}, p={p}")
		
		
	straight = streak(path)
	#print(f"straight={straight}")
	
	if p == (len(grid)-1, len(grid[0])-1) and straight >= 4:
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
			
	past_facings = prev(path)
	
	if (p, past_facings) in visited:
		continue
	#print(f"facing={facing}")
			
	for d in dirs:
		#print(f"d={d}")
		p2 = add(p, d)
		if not in_bounds(p2):
			continue
		if facing is not None and rot(d, 2) == facing:
			continue
		if straight >= 10 and d == facing:
			continue
		if straight < 4 and facing is not None and d != facing:
			continue
		#print("...use")
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
