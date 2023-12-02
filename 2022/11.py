from collections import deque
from operator import add, sub

class Monkey:
	def __init__(self, monkeys):
		self.inspectcount = 0
		self.monkeys = monkeys
		
	def parse(self):
		while True:
			line = input()
			line = line.strip()
			if line == "":
				break
			if line.startswith("Monkey"):
				self.num = int(line.split()[1][:-1])
			elif line.startswith("Starting items:"):
				self.items = deque([int(c) for c in line[16:].split(", ")])
			elif line.startswith("Operation:"):
				o = line[11:]
				self.o = o
				def run(old):
					ldict = {'old': old}
					exec(o, globals(), ldict)
					new = ldict['new']
					#print(f"    > exec {o}: {old} -> {new}")
					return new
				self.op = run
			elif line.startswith("Test:"):
				self.div = int(line.split()[3])
				self.to = list(reversed([int(input().split()[-1]), int(input().split()[-1])]))
	def __str__(self):
		return f"Monkey {self.num}: count = {self.inspectcount}, items = {self.items}, op = `{self.o}`, test = divisible by {self.div}, throw to = {self.to}"
	
	def get_items(self):
		return f"Monkey {self.num}: count = {self.inspectcount}, items = {self.items}"
	
	def inspect(self):
		while len(self.items) > 0:
			old = self.items.popleft()
			new = self.op(old)
			new = new // 3
			#print(f"    old: {old}, new: {new}")
			if new % self.div == 0:
				self.monkeys[self.to[1]].items.append(new)
			else:
				self.monkeys[self.to[0]].items.append(new)
			self.inspectcount += 1

monkeys = []

while True:
	try:
		m = Monkey(monkeys)
		m.parse()
		print(m)
		monkeys.append(m)
	except EOFError:
		break
		
def print_monkeys():
	global monkeys
	for m in monkeys:
		print(f"   {m.get_items()}")
		
for i in range(20):
	for j, m in enumerate(monkeys):
		# print(f"inspect {j}")
		m.inspect()
	print(f"round {i+1}:")
	print_monkeys()
	bus = list(sorted([m.inspectcount for m in monkeys], reverse=True))
	print(f"monkey business: {bus[0] * bus[1]}")
