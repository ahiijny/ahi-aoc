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
	
	grid[(a, r)] = '#'
	
def getbounds():
	global grid
	
	minx = min(a[0]-r for a,r in grid.keys())
	maxx = max(a[0]+r for a,r in grid.keys())
	miny = min(a[1]-r for a,r in grid.keys())
	maxy = max(a[1]+r for a,r in grid.keys())
	return minx, maxx, miny, maxy
	
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
	draw(s, radii[s])
	
# sprint(f"grid: {grid}")

#test_y = 10
test_y = 2000000
count = 0

minx, maxx, miny, maxy = getbounds()

print(f"bounding box: x = [{minx}..{maxx}], y = [{miny}..{maxy}]")

for x in range(minx, maxx+1):
	if x % 10000 == 0:
		print(f"checking x = {x}, count = {count}")
	if is_not_beacon((x, test_y)):
		count += 1
		
print(f"items at y={test_y}: {count}")

