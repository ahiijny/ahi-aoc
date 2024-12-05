lines = []
safes = []
num_safe = 0

try:
	while True:
		line = [int(a) for a in input().split()]
		
		for i in range(len(line)):
			sublist = line[:i] + line[i+1:]
			diffs = [sublist[i+1] - sublist[i] for i in range(len(sublist) - 1)]
			all_increasing = all(d > 0 for d in diffs)
			all_decreasing = all(d < 0 for d in diffs)
			safe = all(1 <= abs(d) and abs(d) <= 3 for d in diffs)
			if (all_increasing or all_decreasing) and safe:
				num_safe += 1
				break
except EOFError:
	pass
	
print(num_safe)
	

	
