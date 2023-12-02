from collections import deque
from operator import add, sub

bases = set()

class Worry:
	def __init__(self, value):
		if isinstance(value, Worry):
			self.values = {}
			for k, v in value.values.items():
				self.values[k] = v
		else:
			self.orig = int(value)
			self.values = {}
			global bases
			for base in bases:
				self.values[base] = self.orig % base
	
	def update(self, base, value):
		value = value % base
		self.values[base] = value
	
	def __str__(self):
		return str(self.values)
		
	def __repr__(self):
		return str(self)

class Monkey:
	def __init__(self, monkeys):
		self.inspectcount = 0
		self.monkeys = monkeys
		self.items = []
		
	def parse(self):
		while True:
			line = input()
			line = line.strip()
			if line == "":
				break
			if line.startswith("Monkey"):
				self.num = int(line.split()[1][:-1])
			elif line.startswith("Starting items:"):
				self.rawitems = deque([int(c) for c in line[16:].split(", ")])
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
	
	def init_items(self):
		self.items = deque([Worry(c) for c in self.rawitems])
				
	def __str__(self):
		return f"Monkey {self.num}: count = {self.inspectcount}, origitems = {self.rawitems}, items = {self.items}, op = `{self.o}`, test = divisible by {self.div}, throw to = {self.to}"
	
	def get_items(self):
		return f"Monkey {self.num}: count = {self.inspectcount}, items = {self.items}"
	
	def inspect(self):
		global bases
		while len(self.items) > 0:
			old = self.items.popleft()
			# print(f"old: {old}")
			new = Worry(old)
			
			for base in bases:
				new.update(base, self.op(old.values[base]))
			#print(f"    old: {old}, new: {new}")
			if new.values[base] % self.div == 0:
				self.monkeys[self.to[1]].items.append(new)
			else:
				self.monkeys[self.to[0]].items.append(new)
			self.inspectcount += 1

monkeys = []

while True:
	try:
		m = Monkey(monkeys)
		m.parse()
		bases.add(m.div)
		print(m)
		monkeys.append(m)
	except EOFError:
		break
		
print(f"bases: {bases}")

mega = 1

for b in bases:
	mega *= b
	
bases = {mega}

for m in monkeys:
	m.init_items()

def print_monkeys():
	global monkeys
	for m in monkeys:
		print(f"   {m.get_items()}")
		
for i in range(10000):
	for j, m in enumerate(monkeys):
		# print(f"inspect {j}")
		m.inspect()
	if (i+1) % 1000 == 0:
		print(f"round {i+1}:")
		print_monkeys()
		bus = list(sorted([m.inspectcount for m in monkeys], reverse=True))
		print(f"monkey business: {bus[0] * bus[1]}")
