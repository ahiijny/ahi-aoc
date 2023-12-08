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

ends = []

for j in range(len(curs)):
	s = 0
	cur = curs[j]
	ends.append([])
	while s < loops[j][0]:
		for i,ins in enumerate(instr):
			if ins == 'R':
				cur = tree[cur][1]
			else:
				cur = tree[cur][0]
			s += 1
			if cur[-1] == 'Z':
				ends[j].append(s)
			if s == loops[j][0]:
				break
				
print(f"ends={ends}")


a = []
b = []
m = []

for j in range(len(curs)):
	a.append(loops[j][1])
	b.append(loops[j][0])
	m.append(b[-1] - a[-1])

# calc lcm

print(f"{math.lcm(*m)}")
