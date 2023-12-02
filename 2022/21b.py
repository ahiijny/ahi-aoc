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
			if name == 'humn':
				val = '?'
			monkeys[name] = val
		else:
			op1 = cmd[1]
			op = cmd[2]
			if name == 'root':
				op = '='
			op2 = cmd[3]
			monkeys[name] = [op, op1, op2]
		
	except EOFError:
		break

print(f"{monkeys}")

class Node:
	def __init__(self, monkeys=None, name=None, val=None, op=None, children=None):
		self.monkeys = monkeys
		self.name = name
		self.val = val
		self.op = op
		self.children = children
		
		if name is not None:
			x = self.monkeys[name]
			if type(x) != list:
				self.val = x
			else:
				self.op = x[0]
				self.children = [Node(monkeys, x[1]), Node(monkeys, x[2])]
			
	def has(self, name):
		if self.name == name:
			return True
		elif self.children is not None:
			if self.children[0].has(name):
				return True
			elif self.children[1].has(name):
				return True
		return False
		
	def rotate(self, new_left, new_right_op, new_right_left, new_right_right):
		self.children[0] = new_left
		new_right = Node(op=new_right_op, children=[new_right_left, new_right_right])
		self.children[1] = new_right
		
	def solve(self, x):
		assert self.op == '='
		# put unknown on left side
		if self.children[1].has(x):
			self.children.reverse()
		while self.children[0].name != x:
			left = self.children[0]
			child_with_x = 0
			if self.children[0].children[1].has(x):
				child_with_x = 1
			
			if self.children[0].op == '+':
				if child_with_x == 1:
					left.children.reverse()
				self.rotate(left.children[0], '-', self.children[1], left.children[1])
			elif self.children[0].op == '-':
				if child_with_x == 0:
					self.rotate(left.children[0], '+', self.children[1], left.children[1])
				else:
					left.children.reverse()
					node = Node(op='*', children=[Node(val=-1), self.children[1]])
					self.children[1] = node
			elif self.children[0].op == '*':
				if child_with_x == 1:
					left.children.reverse()
				self.rotate(left.children[0], '/', self.children[1], left.children[1])
			elif self.children[0].op == '/':
				if child_with_x == 0:
					self.rotate(left.children[0], '*', self.children[1], left.children[1])
				else:
					left.children.reverse()
					node = Node(op='/', children=[Node(val=1), self.children[1]])
					self.children[1] = node
			
	def calc(self):
		if self.val is not None:
			return int(self.val)
		else:
			self.children[0].calc()
			self.children[1].calc()
			if self.op == '+':
				self.val = self.children[0].val + self.children[1].val
			elif self.op == '-':
				self.val = self.children[0].val - self.children[1].val
			elif self.op == '*':
				self.val = self.children[0].val * self.children[1].val
			elif self.op == '/':
				self.val = self.children[0].val / self.children[1].val
			return self.val
		
	def __repr__(self):
		return str(self)
	
	def __str__(self, depth=0):
		return ("  " * depth) + f"> {self.name}: " + ((f" ({str(self.val)})") if self.val is not None else '') + ((f" {self.op}:\n" + self.children[0].__str__(depth=depth+1) + self.children[1].__str__(depth=depth+1)) if self.children is not None else "") + ('\n' if self.children is None else '')

		
root = Node(monkeys, 'root')

print(f"tree:\n{root}")

root.solve('humn')
root.children[1].calc()

print(f"solved tree:\n{root}")

print(f"value of humn: {root.children[1].val}")