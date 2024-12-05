grid = []
used = []

try:
	while True:
		line = input()
		grid.append(line)
except EOFError:
	pass

H = len(grid)
W = len(grid[0])

used = [[False for x in range(W)] for y in range(H)]

	
masks = [
	['M.S',
	'.A.',
	'M.S'],
	['M.M',
	'.A.',
	'S.S'],
	['S.M',
	'.A.',
	'S.M'],
	['S.S',
	'.A.',
	'M.M'],
]
matches = 0

def match(x, y, mask):
	for my in range(len(mask)):
		for mx in range(len(mask[0])):
			px = x + mx
			py = y + my
			if mask[my][mx] == '.' or mask[my][mx] == grid[py][px]:
				continue
			else:
				#print(f"x={x},y={y},px={px},py={py}, mismatch: {mask[my][mx]} != {grid[py][px]}")
				return False
	for my in range(len(mask)):
		for mx in range(len(mask[0])):
			px = x + mx
			py = y + my
			if mask[my][mx] != '.':
				used[py][px] =  True
	return True

for m in masks:
	for y in range(H-len(m)+1):
		for x in range(W-len(m[0])+1):
			if match(x, y, m):
				matches += 1
				
def print_used():
	for y in range(H):
		for x in range(W):
			if used[y][x]:
				print(grid[y][x], end='')
			else:
				print('.', end='')
		print()
		
print_used()

print(matches)