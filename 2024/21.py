import heapq

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

dirs = {
	'<': (-1, 0),
	'^': (0, -1),
	'>': (1, 0),
	'V': (0,1)
}
	
grid = []
S = None
E = None

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

def get_walk_cache(pad, max_walk):
	shortest_path = {}
	for y in range(len(pad)):
		for x in range(len(pad[y])):
			if pad[y][x] is None:
				continue
			start = pad[y][x]
			p0 = (x,y)
			
			q = []
			q.append(([p0], []))
			shortest_path[(p0, p0)] = ''
			while len(q) > 0:
				path, deltas = q.pop()
				if len(deltas) >= max_walk:
					continue
				if len(deltas) > len(shortest_path[(path[0], path[-1])]):
					continue
				p = path[-1]
				for di, d in dirs.items():
					p2 = add(p, d)
					if bounds(pad, p2[0], p2[1]) and pad[p2[1]][p2[0]] is not None:
						path2 = path + [p2]
						deltas2 = deltas + [di]
						len2 = len(deltas2)
						if (p0, p2) not in shortest_path or len(shortest_path[(p0, p2)]) > len2:
							shortest_path[(p0, p2)] = ''.join(deltas2)
							q.append((path2, deltas2))
	modified_shortest_path = {}
	
	for k,v in shortest_path.items():
		s1 = k[0]
		s2 = k[1]
		start = pad[s1[1]][s1[0]]
		end = pad[s2[1]][s2[0]]
		modified_shortest_path[(start, end)] = v
	return modified_shortest_path

num_shortest_path = get_walk_cache(numpad, 5)
dir_shortest_path = get_walk_cache(dirpad, 3)

print(f"num_shortest_path: {num_shortest_path}")
print(f"dir_shortest_path: {dir_shortest_path}")

def get_seq(shortest_path, start, code):
	moves = []
	cur = start
	for c in code:
		order = (cur, c)
		seq = shortest_path[order]
		moves.append(seq)
		cur = c
	return moves, cur
	
cur1 = 'A'
cur2 = 'A'
cur3 = 'A'
cur4 = 'A'

total = 0

def push_seq(moves):
	return ''.join([m + 'A' for m in moves])

for code in codes:
	print(f">code: {code}")
	seq, cur1 = get_seq(num_shortest_path, cur1, code)
	print(f"  numpad seq: {seq}")
	seq2, cur2 = get_seq(dir_shortest_path, cur2, push_seq(seq))
	print(f"  dirpad 1 seq: {seq2}")
	seq3, cur3 = get_seq(dir_shortest_path, cur3, push_seq(seq2))
	print(f"  dirpad 2 seq: {seq3}")
	
	length = len(push_seq(seq3))
	print(f" length={length}")
	numeric = int(code.replace('A',''))
	complexity = length * numeric
	
	total += complexity
	
print(f"total={total}")