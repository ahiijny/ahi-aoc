lines = []
safes = []
num_safe = 0

try:
	while True:
		line = [int(a) for a in input().split()]
		diffs = [line[i+1] - line[i] for i in range(len(line) - 1)]
		all_increasing = all(d > 0 for d in diffs)
		all_decreasing = all(d < 0 for d in diffs)
		safe = all(1 <= abs(d) and abs(d) <= 3 for d in diffs)
		if (all_increasing or all_decreasing) and safe:
			num_safe += 1
		safes.append(safe)
		lines.append(line)
except EOFError:
	pass
	
#for line, safe in zip(lines, safes):
	#print(line, ":", safe)
	
print(num_safe)
	

	
