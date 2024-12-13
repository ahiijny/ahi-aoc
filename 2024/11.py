nums = [a for a in input().split()]

print(nums)

n = 25

for i in range(n):
	next_nums = []
	
	for j,s in enumerate(nums):
		m = len(s)
		if s == '0':
			next_nums.append('1')
		elif m % 2 == 0:
			next_nums.extend([str(int(s[:m//2])), str(int(s[m//2:]))])
		else:
			next_nums.append(str(int(s) * 2024))
	#print(f'iteration {i}:', ' '.join(next_nums))
	nums = next_nums
	
print(len(nums))
