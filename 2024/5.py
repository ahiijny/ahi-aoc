rules = {}
pages = []


try:
	while True:
		rule = input()
		if rule == "":
			break
		a,b = rule.split("|")
		a = int(a)
		b = int(b)
		if a in rules:
			rules[a].add(b)
		else:
			after = set()
			after.add(b)
			rules[a] = after
		
	while True:
		pages.append([int(a) for a in input().split(",")])
except EOFError:
	pass
valid = [True for i in range(len(pages))]

print(rules)
print(pages)	

for pi, pp in enumerate(pages):
	for i in range(1, len(pp)):
		for j in range(i):
			before = pp[j]
			after = pp[i]
			if after in rules and before in rules[after]:
				valid[pi] = False

total = 0

for i, v in enumerate(valid):
	if v:
		total += pages[i][len(pages[i])//2]
print(total)
		
