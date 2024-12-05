s1 = []
s2 = []

count1 = {}
count2 = {}

try:
	while True:
		a, b = input().split()
		a = int(a)
		b = int(b)
		s1.append(a)
		s2.append(b)
		if a in count1:
			count1[a] += 1
		else:
			count1[a] = 1
		if b in count2:
			count2[b] += 1
		else:
			count2[b] = 1
except EOFError:
	pass
	
sim = 0

for i, s in enumerate(s1):
	if s in count2:
		sim += s * count2[s]
	
print(sim)
