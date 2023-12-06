from math import prod

times = [int(x.strip()) for x in input().split(':')[1].split()]
distances = [int(x.strip()) for x in input().split(':')[1].split()]

print(f"times={times}")
print(f"distances={distances}")

# t1 + t2 = t
# t1 + t1*t2 = d

wins = {}

for i in range(len(times)):
	wins[i] = []
	t = times[i]
	d = distances[i]
	for hold in range(1, t+1):
		record = (t - hold) * hold
		if record > d:
			wins[i].append(hold)
			
print(f"win conditions={wins}")
print(f"ways to win={list(len(w) for w in wins.values())}")
print(f"margin={prod(len(w) for w in wins.values())}")
			