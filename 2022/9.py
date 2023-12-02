from collections import deque
from operator import add, sub

visited = {}

head = [0, 0]
tail = [0, 0]

steer = {
	'R': [1, 0],
	'U': [0, 1],
	'L': [-1, 0],
	'D': [0, -1]
}

def plus(a, b):
	return list(map(add, a, b))
	
def minus(a, b):
	return list(map(sub, a, b))
	
while True:
	try:
		move = input().split()
		delta = steer[move[0]]
		amount = int(move[1])
		
		for i in range(amount):
			visited[tuple(tail)] = True
			head = plus(head, delta)
			if abs(head[0] - tail[0]) <= 1 and abs(head[1] - tail[1]) <= 1:
				continue
			if abs(head[0] - tail[0]) > 1 or abs(head[1] - tail[1]) > 1:
				delta2 = list(delta)
				if abs(head[0] - tail[0]) == 1:
					delta2[0] = head[0] - tail[0]
				elif abs(head[1] - tail[1]) == 1:
					delta2[1] = head[1] - tail[1]					
				tail = plus(tail, delta2)
				visited[tuple(tail)] = True
	except EOFError:
		break
		
print(f"visited: {visited}")
print(f"visited: {len(visited)}")
	
	
