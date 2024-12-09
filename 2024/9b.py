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
			
			
l1 = 0
l2 = 0
r1 = len(mem) - 1
r2 = len(mem) - 1

while r1 >= m[0]:
	while mem[r2] == '.' and r2 > 0:
		r2 -= 1
	idnum = mem[r2]
	r1 = r2
	while mem[r1] == idnum and r1 > 0:
		r1 -= 1
	r1 += 1
	while mem[l1] != '.' and l1 < len(mem) - 1:
		l1 += 1
	idnum = mem[l1]
	l2 = l1
	while mem[l2] == idnum and l2 < len(mem) - 1:
		l2 += 1
	l2 -= 1
	
	# l1..l2 and r1..r2 point to earliest next gap and latest next file
	if r1 <= l1:
		r2 = r1 - 1
		r1 = r2
		l1 = 0
		l2 = 0
		continue
	
	if l2 - l1 + 1 < r2 - r1 + 1:
		l1 = l2 + 1
		l2 = l1
	else:
		for j in range(r2 - r1 + 1):
			mem[l1+j], mem[r1+j] = mem[r1+j], mem[l1+j]
		l1 = 0
		l2 = 0
		
print(''.join([str(x)+'|' for x in mem]))
	
total = 0
for i,b in enumerate(mem):
	if b == '.':
		continue
	total += b * i
	
print(f"checksum={total}")