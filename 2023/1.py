import re

total = 0

replace = {
	'one': 1,
	'two': 2,
	'three': 3,
	'four': 4,
	'five': 5,
	'six': 6,
	'seven': 7,
	'eight': 8,
	'nine': 9,
}
while True:
	try:
		first = None
		last = None
		line = input()
		for i in range(len(line)):
			for word, digit in replace.items():
				if line[i:].startswith(word):
					last = digit
					if first is None:
						first = digit
			if line[i].isdigit():
				last = int(line[i])
				if first is None:
					first = last
		print(f"digits={first},{last}")
		total += first * 10 + last
	except EOFError:
		break

print(f"total: {total}")
