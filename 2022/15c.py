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
	
def get_perim_walk(a, r):
	#print(f"perim walk {a} radius {r}:")
	x = a[0]
	y = a[1]
	
	seats = [(x, y-r), (x+r, y), (x, y+r), (x-r, y), (x, y-r)]
	incrs = [
		[1, 1],
		[-1, 1],
		[-1, -1],
		[1, -1]
	]
	
	next_seat_idx = 1
	incr_idx = 0
	
	p = list(seats[0])
	yield tuple(p)
	
	while True:
		p[0] += incrs[incr_idx][0]
		p[1] += incrs[incr_idx][1]
		yield tuple(p)
		
		if tuple(p) == seats[next_seat_idx]:
			next_seat_idx +=1
			incr_idx += 1
		
			if incr_idx >= len(incrs):
				return
	
def getbounds():
	global grid
	
	minx = min(a[0]-r for a,r in grid.keys())
	maxx = max(a[0]+r for a,r in grid.keys())
	miny = min(a[1]-r for a,r in grid.keys())
	maxy = max(a[1]+r for a,r in grid.keys())
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
			elif is_not_beacon((x,y)):
				print('#', end='')
			else:
				print('.', end='')
		print()
	
def is_not_beacon(p):
	global grid
	
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


minx = 0
maxx = 4000000
#maxx = 20
miny = 0
#maxy = 20
maxy = 4000000

print(f"bounding box: x = [{minx}..{maxx}], y = [{miny}..{maxy}]")

def search():
	count = 0
	for a,r in grid.keys():
		print(f"checking extend perimeter+1 of sensor {a} with radius {r}...")
		for p in get_perim_walk(a, r+1):
			count += 1
			if count % 1000000 == 0:
				print(f"...currently checking {p}, total checked = {count}")
			if minx <= p[0] and p[0] <= maxx and miny <= p[1] and p[1] <= maxy:
				if not is_not_beacon(p):
					print(f"found beacon at {p}")
					return			

search()
