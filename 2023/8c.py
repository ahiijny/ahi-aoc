instr = input()

input()

tree = {}

while True:
	try:
		nodes = input().split("=")
		node = nodes[0].strip()
		adj = nodes[1].split(",")
		left = adj[0].strip()[1:]
		right = adj[1].strip()[:-1]
		
		tree[node] = (left, right)
	except EOFError:
		break
		
print(f"tree: {tree}")

cur = []
for c in tree.keys():
	if c[-1] == 'A':
		cur.append(c)
		
steps = 0

print(f"starts: {cur}")

while not all(c[-1] == 'Z' for c in cur):
	for i in instr:
		for j in range(len(cur)):				
			if i == 'R':
				cur[j] = tree[cur[j]][1]
			else:
				cur[j] = tree[cur[j]][0]
		steps += 1
		if steps % 10000 == 0:
			print(f"steps={steps}")
		# print(f' -> {cur}')
		if all(c[-1] == 'Z' for c in cur):
			break
		
print(f"steps: {steps}")
	