import ast
import re
from copy import deepcopy
from collections import deque
import math

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
		
def split_int(intervals, var, at):
	# [2, 5) @ 3 -> [2, 3), [3, 5)
	r = intervals[var]
	if at < r[0]:
		return (None, intervals)
	elif at >= r[1]:
		return (intervals, None)
	
	i1 = intervals
	i2 = deepcopy(intervals)
	i1[var][1] = at
	i2[var][0] = at
	
	return (i1, i2)
		
def process(intervals):
	print(f"testing {intervals}")
	A = []
	R = []
	
	q = deque()
	q.appendleft((intervals, 'in'))
	
	while len(q) > 0:
		intervals, w_name = q.popleft()
		
		print(f" -> {w_name} @ {intervals}")
		if w_name == 'A':
			A.append(intervals)
			continue
		elif w_name == 'R':
			R.append(intervals)
			continue
		
		w = workflows[w_name]
		
		rules = w[w.index('{')+1:w.index('}')].split(',')
		for rule in rules:
			if intervals is None:
				break
			if ':' in rule:
				split = rule.split(':')
				cond = split[0]
				target_name = split[1]
				
				if '>' in cond:
					cond = cond.split('>')
					var = cond[0]
					value = int(cond[1])
					
					# > 5 -> [.., 6), [6, ...]
					(a, b) = split_int(intervals, var, value+1)
					if b is not None:
						q.appendleft((b, target_name))
					intervals = a
				elif '<' in cond:
					cond = cond.split('<')
					var = cond[0]
					value = int(cond[1])
					
					# < 5 -> [.., 5), [5, ...)
					(a, b) = split_int(intervals, var, value)
					if a is not None:
						q.appendleft((a, target_name))
					intervals = b
			else:
				target_name = rule
				q.appendleft((intervals, target_name))
	return A, R

print(f"workflows: {workflows}")
print(f"items: {items}")

total = 0

intervals = {
	'x': [1, 4001], # [start, end) intervals
	'm': [1, 4001],
	'a': [1, 4001],
	's': [1, 4001],
}

A, R = process(intervals)

total = 0

for intervals in A:
	print(f"accepted interval {intervals}")
	combinations = math.prod([x[1] - x[0] for x in intervals.values()])
	total += combinations
	
print(f"total = {total}")