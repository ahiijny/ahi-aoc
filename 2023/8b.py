import math

instr = input()

input()

tree = {}

while True:
	try:
		nodes = input().split("=")
		node = nodes[0].strip()
		adj = nodes[1].split(",")
		left = adj[0].strip()[1:]
		right = adj[1].strip()[:-1]
		
		tree[node] = (left, right)
	except EOFError:
		break
		
print(f"tree: {tree}")

curs = []
for c in tree.keys():
	if c[-1] == 'A':
		curs.append(c)
		
steps = 0

print(f"starts: {curs}")

# loop finder

loops = []

for j in range(len(curs)):
	cur = curs[j]
	hist = {(cur, 0): 0}
	s = 0
	while len(loops) <= j:
		for i,ins in enumerate(instr):
			if ins == 'R':
				cur = tree[cur][1]
			else:
				cur = tree[cur][0]
			s += 1
			if (cur, i+1) not in hist:
				hist[(cur, i+1)] = s
			else:
				print(f"loop found for start={curs[j]}: ({cur}, inst={i+1}) at s={hist[(cur, i+1)]} and s={s}")
				loops.append((s, hist[(cur, i+1)], cur, i+1))
				break

ends = [] # only one end per loop

for j in range(len(curs)):
	s = 0
	cur = curs[j]
	while s < loops[j][0] and len(ends) <= j:
		for i,ins in enumerate(instr):
			if ins == 'R':
				cur = tree[cur][1]
			else:
				cur = tree[cur][0]
			s += 1
			if cur[-1] == 'Z':
				ends.append(s)
				break
				
print(f"ends={ends}")
	
# loops at 0-a-b-a-b
# e.g.
#		0 .. 2 .. 40
#		0 .. 3 .. 37
# node for ghost j at step s is equal to (s - a) % (b - a) + a
# e.g. for ghost 1: position 40 is same as 2. so (40 - 2) % 38 + 2 == 2
# so we want an equation for p0(e0) = p1(e1)
# i.e. e0 % (b0 - a0) == e1 % (b1 - a1) == ...
# or e0 + k0 * (b0 - a0) == e1 + k1 * (b1 - a1)

a = []
b = []
m = []

for j in range(len(curs)):
	a.append(loops[j][1])
	b.append(loops[j][0])
	m.append(b[-1] - a[-1])
	
s = ends[0]
multiplier = m[0]

for j in range(1, len(ends)):
	while s != ends[j] % m[j]:
		s += multiplier
		print(f"j={j}, s={s}")