import heapq
import functools
from collections import deque

numpad = [
	['7','8','9'],
	['4','5','6'],
	['1','2','3'],
	[None, '0', 'A']
]

dirpad = [
	[None, '^', 'A'],
	['<', 'V', '>']
]

pads = [
	numpad,
	dirpad
]

dirs = {
	'<': (-1, 0),
	'^': (0, -1),
	'>': (1, 0),
	'V': (0,1)
}

num_to_loc = {}
dir_to_loc = {}

char_to_locs = [
	num_to_loc,
	dir_to_loc
]

for y in range(len(numpad)):
	for x in range(len(numpad[y])):
		if numpad[y][x] is not None:
			num_to_loc[numpad[y][x]] = (x,y)

for y in range(len(dirpad)):
	for x in range(len(dirpad[y])):
		if dirpad[y][x] is not None:
			dir_to_loc[dirpad[y][x]] = (x,y)

def bounds(grid, x, y):
	return 0 <= x and x < len(grid[0]) and 0 <= y and y < len(grid)
	
def add(p1, p2):
	return (p1[0] + p2[0], p1[1] + p2[1])
	
def mul(p, s):
	return (p[0] * s, p[1] * s)
	
codes = []

try:
	while True:
		codes.append(input())
except EOFError:
	pass
	
print(codes)

@functools.cache
def opt(pad_idxs, code):
	#print(f">opt({pad_idxs}, {code})")
	if len(pad_idxs) == 1:
		# just press the keys with finger
		return [code]

	pad_idx = pad_idxs[0]
	pad = pads[pad_idx]
	next_pad_idxs = pad_idxs[1:]
	char_to_loc = char_to_locs[pad_idx]
	max_length = len(pad) - 1 + len(pad[0]) - 1 # path should not ever exceed taxicab geometry of grid
	
	# need to search all possible press sequences because order matters
	# e.g. <V< is less efficient than V<< because needs more movements on the next pad
	
	# every key press should return to A so each individual key press should be independent
	
	cur = 'A'
	super_seq = None
	
	# for each c in code, buttons pressed on next pad need to move finger to 
	# button and then press A
	for c in code:
		start = char_to_loc[cur]
		dest = char_to_loc[c]
		routes = set()
		q = deque()
		q.append(([start], []))
		while len(q) > 0:
			locs, deltas = q.popleft()
			#print(f"bfs: locs={locs}, deltas={deltas}")
			p = locs[-1]
			if p == dest:
				routes.add(''.join(deltas))
				continue
			for di, d in dirs.items():
				p2 = add(p, d)
				if bounds(pad, p2[0], p2[1]) and pad[p2[1]][p2[0]] is not None:
					locs2 = locs + [p2]
					deltas2 = deltas + [di]
					len2 = len(deltas2)
					if len2 <= max_length:
						q.append((locs2, deltas2))
		#print(f"routes from {cur} to {c}: {routes}")
		best_root_len = None
		best_seqs = None
		best_route = None
		for r in routes:
			next_code = r + 'A'
			opt_seqs = opt(next_pad_idxs, next_code)
			if best_root_len is None or best_root_len > len(opt_seqs[-1]):
				best_root_len = len(opt_seqs[-1])
				best_seqs = opt_seqs
				best_route = next_code
		
		if super_seq is None:
			super_seq = [best_route] + best_seqs
		else:
			super_seq[0] = super_seq[0] + best_route
			for i in range(1, len(super_seq)):
				super_seq[i] = super_seq[i] + best_seqs[i-1]
		cur = c
	return super_seq

total = 0
		
for code in codes:
	opt_seq = opt((0, 1, 1, 1), code)
	print(f">code: {code}")
	for i, seq in enumerate(opt_seq):
		print(f"  seq {i} = {seq}, len = {len(seq)}")
	numeric = int(code.replace('A',''))
	complexity = len(seq) * numeric
	
	total += complexity
		
print(total)