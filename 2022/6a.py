from collections import deque

while True:
	try:
		buffer = deque()
		line = input()
		for i, ch in enumerate(line):
			buffer.append(ch)
			if len(buffer) > 14:
				buffer.popleft()
			# print(buffer)
			# print(len(set(buffer)))
			if len(set(buffer)) == 14:
				print(f"found marker: {i+1}")
				break
	except EOFError:
		break

