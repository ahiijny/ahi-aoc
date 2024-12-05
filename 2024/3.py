import re

mem = []

try:
	while True:
		line = input()
		mem += list(line)
except EOFError:
	pass
	
#print(mem)

total = 0

for match in re.finditer("mul\\((\\d+),(\\d+)\\)", ''.join(mem)):
	a = match.group(1)
	b = match.group(2)
	subsum = int(a)*int(b)
	print(f"{a} x {b} = {subsum}")
	total += subsum
	
print(total)
	
	
