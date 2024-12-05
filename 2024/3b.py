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
enabled = True

for match in re.finditer("mul\\((\\d+),(\\d+)\\)|do\\(\\)|don't\\(\\)", ''.join(mem)):
	print(match.group(0))
	if match.group(0).startswith("do()"):
		print("do")
		enabled = True
	elif match.group(0).startswith("don't()"):
		print("don't")
		enabled = False
	else:
		if not enabled:
			print(f"skip {match.group(0)}")
			continue
		a = match.group(1)
		b = match.group(2)
		subsum = int(a)*int(b)
		print(f"{a} x {b} = {subsum}")
		total += subsum
	
print(total)
	
	
