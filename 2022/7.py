from collections import deque

class Node:
	def __init__(self, name):
		self.parent = None
		self.children = {}
		self.name = name
		self.size = 0
		self.subsize = 0
		
	def add(self, child):
		self.children[child.name] = child
		child.parent = self
		
	def get_cd(self, name):
		if name in self.children:
			return self.children[name]
		elif name == '..':
			return self.parent
		node = Node(name)
		self.add(node)
		return node
		
	def get_child(self, entry):
		name = entry[1]
		if name in self.children:
			return self.children[name]
		node = Node(name)
		if entry[0] != 'dir':
			size = int(entry[0])
			node.size = size
		self.add(node)
		return node
		
	def calc_subsize(self):
		for child in self.children.values():
			child.calc_subsize()
		self.subsize = self.size + sum([c.subsize for c in self.children.values()])
		
	def __str__(self, depth=0):
		ch = '>' if self.size == 0 else '|'
		return ("    " * depth) + f" {ch} '" + self.name + "' " + str(self.size) + " (" + str(self.subsize) + ")\n" + "".join([child.__str__(depth+1) for child in self.children.values()])
		
	def sum_subsizes(self, limit): # only count dirs
		total = 0
		if self.size != 0:
			return 0
		if self.subsize <= limit:
			total += self.subsize
		for child in self.children.values():
			total += child.sum_subsizes(limit)
		return total
	
	def find_dir_sizes(self):
		sizes = []
		if self.size == 0:
			sizes.append(self.subsize)
		for child in self.children.values():
			sizes.extend(child.find_dir_sizes())
		return sizes
			
data = []

while True:
	try:
		line = input().split()
		data.append(line)
	except EOFError:
		break
		
i = 0
root = Node("")
pwd = root

while i < len(data):
	cmd = data[i]
	if cmd[0] == '$':
		if cmd[1] == 'cd':
			pwd = pwd.get_cd(cmd[2])
		elif cmd[1] == 'ls':
			while i+1 < len(data) and data[i+1][0] != '$':
				i += 1
				entry = data[i]
				pwd.get_child(entry)
	else:
		raise ValueError("shouldn't happen")
	i += 1
		
root.calc_subsize()
print(f"tree: {root}")
print(f"sum of dirs <= 100000: {root.children['/'].sum_subsizes(100000)}")

sizes = root.children['/'].find_dir_sizes()
sizes = sorted(sizes)
print(f"all dir sizes: {sizes}")

total_space = root.children['/'].subsize
remaining = 70000000 - total_space
req = 30000000 - remaining

for size in sizes:
	if size >= req:
		print(f"delete dir with size {size} to free up at least {req} space")	
		break