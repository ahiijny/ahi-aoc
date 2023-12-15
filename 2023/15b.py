def h(s):
	c = 0
	for i in range(len(s)):
		c += ord(s[i])
		c *= 17
		c %= 256
	return c
		
		
boxes = [{} for i in range(256)] # ordereddict

while True:
	try:
		ss = input().split(',')
		for s in ss:
			if '-' in s:
				label = s.split('-')[0]
				box = h(label)
				boxes[box].pop(label, '')
			else:
				si = s.split('=')
				label = si[0]
				box = h(label)
				focus = int(si[1])
				boxes[box][label] = focus
	except EOFError:
		break
		
# add up

total = 0

for bi, box in enumerate(boxes):
	for li, lens in enumerate(box.values()):
		total += (bi + 1) * (li + 1) * lens
		
print(total)
		

