from collections import deque

numbers = []

values = {
	'=': -2,
	'-': -1,
	'0': 0,
	'1': 1,
	'2': 2
}

revvalues = {
	-2: '=',
	-1: '-',
	0: '0',
	1: '1',
	2: '2'
}

def unconvert(val):
	global revvalues
	digits = []
	carry = 0
	nextcarry = 0
	while val > 0 or carry > 0:
		#print(f"...val={val}, carry={carry}, digits={digits}")
		rem = val % 5 + carry
		if rem > 2:
			rem -= 5
			nextcarry = 1
		else:
			nextcarry = 0
		digits.append(revvalues[rem])
		carry = nextcarry
		val //= 5
	return ''.join(reversed(digits))
		

def convert(num):
	global values
	digits = reversed(list(num))
	val = 0
	place = 1
	for d in digits:
		val += place * values[d]
		place *= 5
	return val
		

while True:
	try:
		num = input()
		val = convert(num)
		numbers.append(val)
	except EOFError:
		break
		
print(f"numbers: {numbers}")
s = sum(numbers)
print(f"sum: {s}")
print(f"input: {unconvert(s)}")
