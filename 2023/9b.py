ff = []

while True:
	try:
		ff.append([list(int(x.strip()) for x in input().split())[::-1]])
	except EOFError:
		break
		
print(f"ff={ff}")

for f in ff:
	print(	f"s={f[0]}")
	i = 1
	while True:
		f.append([])
		for t in range(len(f[i-1]) - 1):
			f[-1].append(f[i-1][t+1] - f[i-1][t])
		if all(x == 0 for x in f[-1]):
			f[-1].append(0)
			break
		i += 1
	# extrapolate
	i -= 1
	while i > 0:
		f[i-1].append(f[i-1][-1] + f[i][-1])
		i -= 1
		
print(f"ff={ff}")
	
# sum new values

print(f"sum={sum(f[0][-1] for f in ff)}")
	