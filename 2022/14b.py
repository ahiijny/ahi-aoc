from collections import deque
from operator import add, sub

grid = {}

while True:
	try:
		line = [[int(c) for c in p.strip().split(",")] for p in input().split("->")]
		print(f"line: {line}")
		
		# draw lines
		for i in range(len(line)-1):
			x1 = min(line[i][0], line[i+1][0])
			y1 = min(line[i][1], line[i+1][1])
			x2 = max(line[i][0], line[i+1][0])
			y2 = max(line[i][1], line[i+1][1])
			
			if x1 == x2:
				for y in range(y1, y2+1):
					grid[(x1, y)] = '#'
			elif y1 == y2:
				for x in range(x1, x2+1):
					grid[(x, y1)] = '#'
		
	except EOFError:
		break

floor = max(p[1] for p in grid.keys())+2

def draw():
	global grid
	global floor
	
	minx = min(p[0] for p in grid.keys())
	maxx = max(p[0] for p in grid.keys())
	ceil = min(p[1] for p in grid.keys())
	
	for r in range(floor-ceil+1):
		for c in range(maxx-minx+1):
			y = r+ceil
			x = c+minx
			if (x,y) in grid:
				print(grid[(x,y)], end='')
			elif y == floor:
				print('#', end='')
			else:
				print('.', end='')
		print()
	

print(f"grid: {grid}")
print(f"floor: {floor}")

count = 0
done = False
while not done:
	loc = [500, 0]
	while True:
		if (loc[0], loc[1]+1) not in grid and loc[1]+1 < floor:
			loc[1] += 1
		elif (loc[0]-1, loc[1]+1) not in grid and loc[1]+1 < floor:
			loc[0] -= 1
			loc[1] += 1
		elif (loc[0]+1, loc[1]+1) not in grid and loc[1]+1 < floor:
			loc[0] += 1
			loc[1] += 1
		else:
			grid[(loc[0], loc[1])] = 'o' # rest
			#print(f"rest: {loc}")
			if [loc[0], loc[1]] == [500, 0]: #plugged
				done = True
			count += 1
			break
			
print(f"final: {count}")