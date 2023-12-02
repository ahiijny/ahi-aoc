def priority(ch):
	if ord(ch) >= ord('a') and ord(ch) <= ord('z'):
		return 1 + ord(ch) - ord('a')
	return 27 + ord(ch) - ord('A')

total = 0

while True:
	try:
		sack1 = input()
		sack2 = input()
		sack3 = input()
		
		set1 = set(sack1)
		set2 = set(sack2)
		set3 = set(sack3)
		
		common = list(set1 & set2 & set3)[0]
		
		print(f"common: {common}")
		total += priority(common)
	except EOFError:
		break
		
print(f"total: {total}")
