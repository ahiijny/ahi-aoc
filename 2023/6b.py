from math import prod

time = int(''.join([x.strip() for x in input().split(':')[1].split()]))
distance = int(''.join([x.strip() for x in input().split(':')[1].split()]))

print(f"time={time}")
print(f"distance={distance}")

# t1 + t2 = t
# t1 + t1*t2 = d

wins = []
t = time
d = distance
for hold in range(1, t+1):
	record = (t - hold) * hold
	if record > d:
		wins.append(hold)
			
# print(f"win conditions={wins}")
print(f"ways to win={len(wins)}")
			