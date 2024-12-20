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
counts = []

cache = {}
def solve(p):
	if p in cache:
		return cache[p]
	print(f"  >solve({p})")
	count = 0
	if p in atoms:
		count += 1
		
	for i in range(0, len(p)-1):
		na = p[:i+1]
		if na in atoms:
			count2 = solve(p[i+1:])
			count += 1 * count2
	cache[p] = count
	return count
	
for pi, p in enumerate(patterns):
	print(f"checking pi={pi}, p={p}")
	count = solve(p)
	print(f"...counted {count} different constructions")
	counts.append(count)
print(f"{sum(counts)} different constructions are possible")
		
