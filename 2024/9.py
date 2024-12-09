line = input()

m = [int(s) for s in line]

n = sum(m)

print(f"n={n}")

mem = ['.'] * n

caret = 0


for i, b in enumerate(m):
	if i % 2 == 0:
		idnum = i // 2
		for j in range(b):
			mem[caret + j] = idnum
		caret += b
	else:
		caret += b
		
# print(''.join([str(x)+'|' for x in mem]))
			
			
left = 0
right = len(mem) - 1

while left < right:
	while mem[right] == '.':
		right -= 1
	while mem[left] != '.':
		left += 1
	if right <= left:
		break
	mem[left], mem[right] = mem[right], mem[left]
	
total = 0
for i,b in enumerate(mem):
	if b == '.':
		continue
	total += b * i
	
print(f"checksum={total}")