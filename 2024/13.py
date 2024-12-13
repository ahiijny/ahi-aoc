aa = []
bb = []
pp = []

try:
	while True:
		a = [x.strip() for x in input().split(":")[1].strip().split(",")]
		b = [x.strip() for x in input().split(":")[1].strip().split(",")]
		c = [x.strip() for x in input().split(":")[1].strip().split(",")]
		
		ax = int(a[0][2:])
		ay = int(a[1][2:])
		aa.append((ax, ay))
		
		bx = int(b[0][2:])
		by = int(b[1][2:])
		bb.append((bx, by))
		
		px = int(c[0][2:])
		py = int(c[1][2:])
		pp.append((px, py))
		input()
except EOFError:
	pass
	
print(aa)
print(bb)
print(pp)

n = 100
costs = []
choices = []
for i in range(len(aa)):
	print(f"prize={i}")
	min_cost = None
	best_choice = None
	for u in range(101):
		for v in range(101):
			cost = 3 * u + v
			loc = (u*aa[i][0] + v*bb[i][0], u*aa[i][1] + v*bb[i][1])
			if loc == pp[i] and (min_cost == None or cost < min_cost):
				min_cost = cost
				best_choice = (u, v)
	costs.append(min_cost)
	choices.append(best_choice)
	
print(costs)
print(choices)
	
print(sum([x for x in costs if x is not None]))

