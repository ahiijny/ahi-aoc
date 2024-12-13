nums = [a for a in input().split()]

print(nums)

num_its = 75

count_memo = {}

def count(s, iterations):
	if (s, iterations) in count_memo:
		return count_memo[(s, iterations)]
		
	nums = []
	if iterations == 0:
		count_memo[(s, iterations)] = 1
		return 1
	else:
		m = len(s)
		if s == '0':
			nums = ['1']
		elif m % 2 == 0:
			nums = [str(int(s[:m//2])), str(int(s[m//2:]))]
		else:
			nums = [str(int(s) * 2024)]
		
		total = 0
		for n in nums:
			total += count(n, iterations-1)
		count_memo[(s, iterations)] = total
		print(f"memo: {(s,iterations)} = {total}")
		return total

total = sum(count(s, num_its) for s in nums)

print(total)

