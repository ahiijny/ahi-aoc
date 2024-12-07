import itertools

lines = []

try:
	while True:
		a, b = input().split(':')
		a = int(a)
		b = [int(x) for x in b.strip().split()]
		lines.append((a, b))
except EOFError:
	pass
	
print(lines)

matches = []
total = 0

for a, b in lines:
	for ops in itertools.product('+*', repeat=len(b)-1):
		value = b[0]
		for i,op in enumerate(ops):
			if op == '+':
				value += b[i+1]
			elif op == '*':
				value *= b[i+1]
		if value == a:
			matches.append((a, ops))
			total += a
			break
			
			
print(matches)
print(len(matches))
print(total)
		
	
