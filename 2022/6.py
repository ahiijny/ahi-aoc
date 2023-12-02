from collections import deque

while True:
	try:
		buffer = deque()
		line = input()
		for i, ch in enumerate(line):
			buffer.append(ch)
			if len(buffer) > 4:
				buffer.popleft()
			if len(set(buffer)) == 4:
				print(f"found marker: {i+1}")
				break
		
	except EOFError:
		break
