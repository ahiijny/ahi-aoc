from collections import deque
from operator import add, sub

pairs = []

def cmp(left, right, depth=0):
	print(("  " * depth) + f"cmp: {left} vs. {right}: ", end='')
	if type(left) == int and type(right) == int:
		if left < right:
			print(1)
			return 1
		elif left > right:
			print(-1)
			return -1
		print(0)
		return 0
	elif type(left) == list and type(right) == list:
		for a, b in zip(left, right):
			print()
			res = cmp(a, b, depth+1)
			if res != 0:
				print(("  " * depth) + "> " + str(res))
				return res
		if len(left) < len(right):
			print(1)
			return 1
		elif len(left) > len(right):
			print(-1)
			return -1
		else:
			print(0)
			return 0
	elif type(left) == int:
		print()
		return cmp([left], right, depth+1)
	elif type(right) == int:
		print()
		return cmp(left, [right], depth+1)

i = 1

correct = []

while True:
	try:
		left = eval(input())
		right = eval(input())
		input()
		pairs.append((left, right))
		
		print(f"===pair {i}===")
		c = cmp(left, right)
		
		# print(f">> result:{c}")
		
		if c == 1:
			correct.append(i)
		
		i += 1
	except EOFError:
		break

print(f"correct pairs: {correct}")
print(f"sum of correct pairs: {sum(correct)}")


