x = 0

stacks = []

while True:
	try:
		rows = []
		while True:
			line = input()
			if "1" in line:
				break
				
			row = []
			for i in range(1, len(line), 4):
				row.append(line[i])
			rows.append(row)			
			
			
		print(f"rows: {rows}")
		
		for i in range(len(rows[0])):
			stacks.append([])
		
		for i in range(len(rows) - 1, -1, -1):
			for j in range(len(rows[i])):
				if rows[i][j] != " ":
					stacks[j].append(rows[i][j])
		print(f"stacks: {stacks}")
		
		input()
		while True:
			action = input()
			params = action.split(" ")
			n = int(params[1])
			a = int(params[3])
			b = int(params[5])
			
			print(f"action: {n} : {a}->{b}")
			
			x = []
			
			for i in range(n):
				x.append(stacks[a-1].pop())
			x.reverse()
			stacks[b-1].extend(x)
	except EOFError:
		break
		
tops = ''.join([stack[-1] for stack in stacks])
		
print(f"end: {tops}")
