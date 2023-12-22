bricks = []
grid = {}
locked = {}

def expand(ends):
	if ends[0] == ends[1]:
		return[ends[0]]
	blocks = []
	for c in range(0, 3):
		a = min(ends[0][c], ends[1][c])
		b = max(ends[0][c], ends[1][c])
		if a == b:
			continue
		for x in range(a, b+1):
			p = list(ends[0])
			p[c] = x
			blocks.append(p)
	return blocks
	
def collides(brick):
	for v in brick:
		if tuple(v) in grid:
			return True
		if v[2] < 1:
			return True
	return False

def place(brick):
	for v in brick:
		grid[tuple(v)] = True
		
def rm(brick):
	for v in brick:
		if tuple(v) in grid:
			del grid[tuple(v)]

def cp(brick):
	return [v[:] for v in brick]
	
def unsupported(brick):
	try:
		# print(f"testing {brick}")
		rm(brick)
		test = cp(brick)
		for v in test:
			v[2] -= 1
			if v[2] < 1:
				return False
		return not collides(test)
	finally:
		place(brick)
	
	
def sd(brick, i):
	#print(f"sd brick {i} = {brick}:")
	rm(brick)
	test = cp(brick)
	for v in test:
		v[2] -= 1
	if not collides(test):
		#print(f"... ok, new brick {test} ")
		place(test)
		return test
	else:
		#print(f"cant drop {i} any further, collision at {test}! placing at {brick}")
		#print(f"\t grid: {grid}")
		place(brick)
		locked[i] = True
		return brick
	

while True:
	try:
		ends = [x.split(",") for x in input().split('~')]
		ends = [list(int(c) for c in x) for x in ends]
		blocks = expand(ends)
		bricks.append(blocks)
		print(f"ends={ends}, blocks={blocks}")
	except EOFError:
		break

for brick in bricks:
	place(brick)
print(f"initial grid: {grid}")

order = [[min(v[2] for v in brick), i, brick] for i, brick in enumerate(bricks)]
order.sort()

print(f"bricks by min z: {order}")

for j, o in enumerate(order):
	i = o[1]
	brick = o[2]
	while i not in locked:
		o[2] = sd(o[2], i)
		
print(f"final bricks: {order}")

count = 0	
old_grid = dict(grid)

# test disintegrates
for j, o in enumerate(order):
	grid = dict(old_grid)
	i = o[1]
	brick = o[2]
	rm(brick)
	will_fall = 0
	for k, o2 in enumerate(order):
		if k == j:
			continue	
		if unsupported(o2[2]):
			#print(f"{o2} unsupported after removing {brick}")
			will_fall += 1
			sd(o2[2], o2[1])
	#print(f"i={i}, can_disintegrate={can_disintegrate}")
	count += will_fall
	place(brick)
	
print(f"count={count}")
	