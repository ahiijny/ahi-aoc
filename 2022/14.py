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

floor = max(p[1] for p in grid.keys())

print(f"grid: {grid}")
print(f"floor: {floor}")

count = 0
done = False
while not done:
	loc = [500, 0]
	while True:
		# print(f"  loc: {loc}")
		if (loc[0], loc[1]+1) not in grid:
			loc[1] += 1
		elif (loc[0]-1, loc[1]+1) not in grid:
			loc[0] -= 1
			loc[1] += 1
		elif (loc[0]+1, loc[1]+1) not in grid:
			loc[0] += 1
			loc[1] += 1
		else:
			grid[(loc[0], loc[1])] = 'o' # rest
			count += 1
			break
		if loc[1] > floor:
			print(f"fell to abyss after securing {count} sands")
			done = True
			break

		