from collections import deque
from operator import add, sub
from pprint import pprint
from functools import cmp_to_key

def cmp(left, right, depth=0):
	if type(left) == int and type(right) == int:
		if left < right:
			return -1
		elif left > right:
			return 1
		return 0
	elif type(left) == list and type(right) == list:
		for a, b in zip(left, right):
			res = cmp(a, b, depth+1)
			if res != 0:
				return res
		if len(left) < len(right):
			return -1
		elif len(left) > len(right):
			return 1
		else:
			return 0
	elif type(left) == int:
		return cmp([left], right, depth+1)
	elif type(right) == int:
		return cmp(left, [right], depth+1)
		
packets = []

while True:
	try:
		left = eval(input())
		right = eval(input())
		input()
		packets.extend([left, right])		
	except EOFError:
		break
		
packets.append([[2]])
packets.append([[6]])

# print(f"packets: {packets}")
packets = sorted(packets, key=cmp_to_key(cmp))
print(f"sorted: {packets}")

for i, x in enumerate(packets):
	if x == [[2]]:
		print(f"[[2]] @ {i}")
	elif x == [[6]]:
		print(f"[[6]] @ {i}")
