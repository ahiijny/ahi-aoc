from collections import deque
from operator import add, sub

reg = 1
t = 0

hist = []

cycles = [20, 60, 100, 140, 180, 220]

def advance():
	global hist
	global t
	hist.append(reg)
	t += 1

while True:
	try:
		cmd = input().split()
		
		if cmd[0] == "noop":
			advance()
		elif cmd[0] == "addx":
			advance()
			advance()
			val = int(cmd[1])
			reg += val
	except EOFError:
		break
		
advance()

total = 0

for c in cycles:
	if c > len(hist):
		break
	strength = hist[c-1] * c
	total += strength

print(f"hist: {hist}")
print(f"total: {total}")

	
