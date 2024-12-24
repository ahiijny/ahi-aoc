import itertools

adj = {}

try:
	while True:
		edg = input().split("-")
		a = edg[0]
		b = edg[1]
		if a not in adj:
			adj[a] = set()
		if b not in adj:
			adj[b] = set()
		adj[a].add(b)
		adj[b].add(a)
		
except EOFError:
	pass
	
print(adj)

ott = {}

trios = []

for a in adj:
	neighbours = adj[a]
	
	for others in itertools.combinations(neighbours, 2):
		b = others[0]
		c = others[1]
		
		trio = frozenset([a, b, c])
		if trio in ott:
			continue
		
		valid = True
		if a not in adj[b] or c not in adj[b]:
			valid = False
		if a not in adj[c] or b not in adj[c]:
			valid = False
		ott[trio] = valid
		
		if valid:
			trios.append(trio)
			
print(f"trios: {trios}")
chiefs = []
for t in trios:
	has_t = False
	for c in t:
		if c[0] == 't':
			has_t = True
			chiefs.append(t)
			break
print(chiefs)
print(len(chiefs))