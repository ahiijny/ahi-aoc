from collections import deque
from operator import add, sub

visited = {}

CHAIN_LENGTH = 10
chain = [[0, 0] for i in range(CHAIN_LENGTH)]

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
	
def print_chain():
	maxx = max(c[0] for c in chain)
	maxy = max(c[1] for c in chain)
	L = maxx + 1
	H = maxy + 1
	
	for r in range(H):
		for c in range(L):
			x = c
			y = H-r-1
			found = False
			for i, node in enumerate(chain):	
				if tuple(node) == tuple([x, y]):
					print(f"{i}",end="")
					found = True
					break
			if not found:
				print('.', end="")
			
		print()

def signum(a):
	if a > 0:
		return 1
	elif a < 0:
		return -1
	return 0
	
while True:
	try:
		move = input().split()
		delta = steer[move[0]]
		amount = int(move[1])
		
		print(f"move: {delta} x{amount}: chain: {chain}")
		# print_chain()
		
		for i in range(amount):
			chain[0] = plus(chain[0], delta)
			for j in range(1, CHAIN_LENGTH):
				head = chain[j-1]
				tail = chain[j]
				if j == CHAIN_LENGTH - 1:
					visited[tuple(tail)] = True
				if abs(head[0] - tail[0]) <= 1 and abs(head[1] - tail[1]) <= 1:
					continue
				if abs(head[0] - tail[0]) > 1 or abs(head[1] - tail[1]) > 1:
					delta2 = None
					if abs(head[0] - tail[0]) > 1:
						delta2 = [signum(head[0]-tail[0]), 0]
						if abs(head[1] - tail[1]) >= 1:
							delta2[1] = signum(head[1] - tail[1])
					else:
						delta2 = [0, signum(head[1]-tail[1])]
						if abs(head[0] - tail[0]) >= 1:
							delta2[0] = signum(head[0] - tail[0])
					tail = plus(tail, delta2)
					if j == CHAIN_LENGTH - 1:
						visited[tuple(tail)] = True
				chain[j] = tail
	except EOFError:
		break
		
print(f"visited: {visited}")
print(f"visited: {len(visited)}")
	
	
