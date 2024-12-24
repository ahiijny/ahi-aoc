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

polycules = {}
ships = {}
max_r = None
max_polycule = None

for a in adj:
	neighbours = adj[a]
	for r in range(2, len(neighbours)+1):
		if r not in polycules:
			polycules[r] = set()
			ships[r] = {}
		
		for others in itertools.combinations(neighbours, r):
			polycule = frozenset(list(others) + [a])
			if polycule in ships[r]:
				continue
			
			valid = True
			for o in others:
				if not valid:
					break
				for p in others:
					if o == p:
						continue
					if p not in adj[o]:
						valid = False
						break
			ships[r][polycule] = valid
			if valid and (max_r is None or r > max_r):
				max_r = r
				max_polycule = polycule
			
print(f"max_r={max_r+1}")
print(f"network={','.join(sorted(max_polycule))}")
