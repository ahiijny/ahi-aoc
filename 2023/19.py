import ast
import re

workflows = {}
items = []

while True:
	line = input()
	if not line:
		break
	name = line[:line.index('{')]
	workflows[name] = line
			
while True:
	try:
		line = input()
		line = line.replace("=", ":")
		line = re.sub(r'([xmas])', "'\\1'", line) 
		print(line)
		item = ast.literal_eval(line)
		items.append(item)
	except EOFError:
		break
		
def process(item):
	print(f"testing {item}")
	x = item['x']
	m = item['m']
	a = item['a']
	s = item['s']
	
	w_name = 'in'
	try:
		while True:
			print(f' -> {w_name}', end='')
			if w_name == 'A':
				return True
			elif w_name == 'R':
				return False
			
			w = workflows[w_name]
			
			rules = w[w.index('{')+1:w.index('}')].split(',')
			for rule in rules:
				if ':' in rule:
					split = rule.split(':')
					cond = eval(split[0])
					if cond:
						w_name = split[1]
						break
				else:
					w_name = rule
					break
	finally:
		print()

print(f"workflows: {workflows}")
print(f"items: {items}")

total = 0

for item in items:
	accepted = process(item)
	if accepted:
		total += sum(item.values())
		
print(f"total = {total}")