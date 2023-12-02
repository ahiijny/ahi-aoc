def priority(ch):
	if ord(ch) >= ord('a') and ord(ch) <= ord('z'):
		return 1 + ord(ch) - ord('a')
	return 27 + ord(ch) - ord('A')

total = 0

while True:
	try:
		sack = input()
		n = len(sack)
		a = sack[:n//2]
		b = sack[n//2:n]
		
		seta = set(a)
		setb = set(b)
		
		common = list(seta & setb)[0]
		
		print(f"common: {common}")
		total += priority(common)
	except EOFError:
		break
		
print(f"total: {total}")