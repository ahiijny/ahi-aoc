atoms = None
patterns = []
try:
	atoms = set([a.strip() for a in input().split(",")])
	input()	
	while True:
		pattern = input()
		patterns.append(pattern)
except EOFError:
	pass
	
print(atoms)
print(patterns)
solutions = {}

cache = {}
def solve(p):
	if p in cache:
		return cache[p]
	print(f"  >solve({p})")
	
	if p in atoms:
		cache[p] = [p]
		return [p]
	for i in range(0, len(p)-1):
		na = p[:i+1]
		if na in atoms:
			sol2 = solve(p[i+1:])
			if sol2 is None:
				continue
			cache[p] = [na] + sol2
			return [na] + sol2
	cache[p] = None
	return None
	
for pi, p in enumerate(patterns):
	print(f"checking pi={pi}, p={p}")
	soln = solve(p)
	if soln is not None:
		solutions[pi] = soln
print(f"{len(solutions)} patterns are possible")
		
