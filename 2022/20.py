from collections import deque

items = []
mixed = []

while True:
	try:
		items.append((len(items), int(input())))
		
	except EOFError:
		break
		
mixed = list(items)
		
print(f"list: {items}")
print(f"n={len(items)}")
n = len(items)

for idx, offset in items:
	i = mixed.index((idx, offset))	
	del mixed[i]
	
	i2 = (i + offset) % (n-1)	
	mixed.insert(i2, (idx, offset))
	if n < 10:
		print(f"mixed: {i}->{i2}: {mixed}")

z = None
for i, (idx, offset) in enumerate(mixed):
	if offset == 0:
		z = i

grove = [mixed[(z+1000)%n][1], mixed[(z+2000)%n][1], mixed[(z+3000)%n][1]]

print(f"grove: {grove}")
print(f"sum: {sum(grove)}")
