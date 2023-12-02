from collections import deque

monkeys = {}

while True:
	try:
		cmd = input().replace(':', '').split()
		name = cmd[0]
		val = None
		op1 = None
		op2 = None
		op = None
		if len(cmd) == 2:
			val = int(cmd[1])
			monkeys[name] = val
		else:
			op1 = cmd[1]
			op = cmd[2]
			op2 = cmd[3]
			monkeys[name] = [op, op1, op2]
		
	except EOFError:
		break

print(f"{monkeys}")

def simplify(monkeys, name):
	if type(monkeys[name]) == int:
		return monkeys[name]
	cmd = monkeys[name]
	op = cmd[0]
	op1 = cmd[1]
	op2 = cmd[2]
	if type(monkeys[op1]) != int:
		simplify(monkeys, op1)
	if type(monkeys[op2]) != int:
		simplify(monkeys, op2)
	op1v = monkeys[op1]
	op2v = monkeys[op2]
	if op == '+':
		monkeys[name] = op1v + op2v
	elif op == '*':
		monkeys[name] = op1v * op2v
	elif op == '-':
		monkeys[name] = op1v - op2v
	elif op == '/':
		monkeys[name] = op1v / op2v
	return monkeys[name]
		
simplify(monkeys, 'root')
print(f"root: {monkeys['root']}")
