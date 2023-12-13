import itertools

springs = []
picross = []

while True:
	try:
		p = input().split()
		nus = '?'.join([p[0]] * 5)
		springs.append(list(nus) + ['.']) # add extra
		picross.append([int(d) for d in p[1].split(",")] * 5)
	except EOFError:
		break
		
print(f"springs={springs}")
print(f"picross={picross}")

def validate(s, p):
	on = False
	count = 0
	pi = 0
	if len(p) == 0 and '#' in s:
		return False
		
	for i in range(len(s)):
		if not on:
			if s[i] != '.':
				on = True
				count += 1
		elif on:
			if s[i] == '.':
				on = False
				
				if pi >= len(p):
					return False
				if count != p[pi]:
					return False
				pi += 1				
				count = 0
				
			else:
				count += 1
	if pi < len(p):
		return False
	return True
		
arrangements = []

for i, s in enumerate(springs):
	p = picross[i]
	print(f"s={''.join(s)}, p={p}, valid={validate(s,p)}")
	
	q_locs = []
	for i in range(len(s)):
		if s[i] == '?':
			q_locs.append(i)
			
	# iterate all possibilities
	
	count = 0
	
	for on in itertools.product(['.', '#'], repeat=len(q_locs)):
		for i in range(len(q_locs)):
			s[q_locs[i]] = on[i]
		if validate(s, p):
			count += 1
			# print(f"  valid:{''.join(s)}, p={p}")
	print(f"\t-> num arrangements={count}")
	arrangements.append(count)
	
print(f" => sum={sum(arrangements)}")
	
	

		
