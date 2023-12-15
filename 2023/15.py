def h(s):
	c = 0
	for i in range(len(s)):
		c += ord(s[i])
		c *= 17
		c %= 256
	return c
		

while True:
	try:
		s = input().split(',')
		print(sum(h(i) for i in s))
	except EOFError:
		break
		

