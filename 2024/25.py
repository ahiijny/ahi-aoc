keys = []
locks = []

def convert(key):
	counts = []
	if key[0][0] == '#':
		# pin, let's make negative
		for x in range(len(key[0])):
			for y in range(len(key)):
				if key[y][x] == '.':
					counts.append(-1 * y)
					break
	else:
		for x in range(len(key[0])):
			for y in range(len(key)):
				if key[y][x] == '#':
					counts.append(len(key) - y)
					break
	return key, counts

def match(a, b):
	#print(f"comparing: {a[1]}, {b[1]}")
	ka = a[0]
	ca = a[1]
	kb = b[0]
	cb = b[1]
	
	for c1, c2 in zip(ca, cb):
		if c1 > 0 and c2 > 0 or c1 < 0 and c2 < 0:
			return False
		if abs(c1) + abs(c2) > len(ka):
			return False
	return True

try:
	key = []
	while True:
		line = input()
		if line == "":
			if len(key) == 0:
				continue
			result = convert(key)
			if result[1][0] > 0:
				keys.append(result)
			else:
				locks.append(result)
			key = []
		else:
			key.append(line)
except EOFError:
	pass
	
print(f"keys: {keys}")
print(f"locks: {locks}")

count = 0

for i in range(len(keys)):
	for j in range(len(locks)):
		if match(keys[i], locks[j]):
			print(f"match: {keys[i][1]}, {locks[j][1]}")
			count += 1
print(count)

		
		