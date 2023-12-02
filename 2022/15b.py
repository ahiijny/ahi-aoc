from collections import deque
from operator import add, sub

grid = {}
sensors = {}
beacons = {}
radii = {}


def dist(a, b):
	return abs(b[0] - a[0]) + abs(b[1] - a[1])
	
def draw(a, r):
	global grid
	
	cx = a[0]
	cy = a[1]
	
	count = 0
	
	for y in range(cy-r, cy+r+1):
		for x in range(cx-r, cx+r+1):
			count += 1
			if count % 1000000 == 0:
				print(f"drawing at: {x},{y}")
			if dist(a, (x,y)) <= r:
				grid[(x,y)] = '#'
	
def getbounds():
	global grid
	
	minx = min(x for x,y in grid.keys())
	maxx = max(x for x,y in grid.keys())
	miny = min(y for x,y in grid.keys())
	maxy = max(y for x,y in grid.keys())
	return minx, maxx, miny, maxy
	
def print_grid():
	global grid
	minx, maxx, miny, maxy = getbounds()
	
	for y in range(miny, maxy+1):
		for x in range(minx, maxx+1):
			if (x,y) == (0,0):
				print('0', end='')
			if (x,y) in sensors:
				print('s', end='')
			elif (x,y) in beacons:
				print('B', end='')
			elif (x,y) in grid:
				print('#', end='')
			else:
				print('.', end='')
		print()
	
def is_not_beacon(p):
	global grid
	
	if p in beacons:
		return False
	
	for a,r in grid.keys():
		if dist(p, a) <= r:
			return True
	return False
		

while True:
	try:
		line = input().split()
		x = int(line[2].split('=')[1].replace(',', '').replace(':', ''))
		y = int(line[3].split('=')[1].replace(',', '').replace(':', ''))
		bx = int(line[8].split('=')[1].replace(',', '').replace(':', ''))
		by = int(line[9].split('=')[1].replace(',', '').replace(':', ''))
		sensors[(x,y)] = (bx, by)	
		beacons[(bx, by)] = True
		radii[(x,y)] = dist((x,y), (bx, by))
		
	except EOFError:
		break
		
print(f"sensors: {sensors}")
print(f"radii: {radii}")

for s in sensors.keys():
	print(f"drawing sensor {s} with radius={radii[s]}")
	draw(s, radii[s])
	
minx = 0
maxx = 4000000
#maxx = 20
miny = 0
#maxy = 20
maxy = 4000000

print_grid()

def run():
	global grid
	
	for x in range(minx, maxx+1):
		if x % 10000 == 0:
			print(f"checking x = {x}")
		for y in range(miny, maxy+1):
			if (x,y) not in grid:
				print(f"found at: {(x,y)}")
		
# run()
