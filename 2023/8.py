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

cur = 'AAA'
steps = 0
while cur != 'ZZZ':
	for i in instr:
		if i == 'R':
			cur = tree[cur][1]
		else:
			cur = tree[cur][0]
		steps += 1
		# print(f' -> {cur}')
		if cur == 'ZZZ':
			break
		
print(f"steps: {steps}")
	
		
		
