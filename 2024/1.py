s1 = []
s2 = []

try:
	while True:
		a, b = input().split()
		s1.append(int(a))
		s2.append(int(b))
except EOFError:
	pass
	
s1 = sorted(s1)
s2 = sorted(s2)

diff = sum(abs(a - b) for a,b in zip(s1, s2))
print(diff)
