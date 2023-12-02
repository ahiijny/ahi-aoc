from collections import deque
from operator import add, sub

reg = 1
t = 0
crt = 0

hist = []

cycles = [20, 60, 100, 140, 180, 220]

pixels = [[]]

def advance():
	global hist
	global t
	global crt
	ch = '.'
	if crt == reg or crt == reg-1 or crt == reg+1:
		ch = '#'
	pixels[-1].append(ch)
	crt += 1
	if crt >= 40:
		crt = 0
		pixels.append([])
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

total = 0

for c in cycles:
	if c > len(hist):
		break
	strength = hist[c-1] * c
	total += strength
	
def pgrid():
	for r in pixels:
		print(''.join(r))

print(f"hist: {hist}")
print(f"total: {total}")

pgrid()



	
