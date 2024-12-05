forward = {}
backward = {}
pages = []


try:
	while True:
		rule = input()
		if rule == "":
			break
		a,b = rule.split("|")
		a = int(a)
		b = int(b)
		if a in forward:
			forward[a].add(b)
		else:
			after = set()
			after.add(b)
			forward[a] = after
		if b in backward:
			backward[b].add(a)
		else:
			before = set()
			before.add(a)
			backward[b] = before
		
	while True:
		pages.append([int(a) for a in input().split(",")])
except EOFError:
	pass
valid = [True for i in range(len(pages))]

print(forward)
print(backward)
print(pages)	

for pi, pp in enumerate(pages):
	for i in range(1, len(pp)):
		for j in range(i):
			before = pp[j]
			after = pp[i]
			if after in forward and before in forward[after]:
				valid[pi] = False

total = 0

for i, v in enumerate(valid):
	if v:
		total += pages[i][len(pages[i])//2]
		
def swap(pages, i, j):
	pages[j], pages[i] = pages[i], pages[j]

new_total = 0

for i, v in enumerate(valid):
	if not v:
		pp = pages[i]
		for j in range(len(pp)-1, 0, -1):
			for i in range(j-1, -1, -1):
				# i should occur before j
				# if i must go after j, it is a violation
				if pp[j] in forward and pp[i] in forward[pp[j]]:
					swap(pp, i, j)
		new_total += pp[len(pp)//2]
		
print(new_total)
		
		
