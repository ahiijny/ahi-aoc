nums = []
nexts = []

try:
	while True:
		nums.append(int(input()))
except EOFError:
	pass
nexts = list(nums)	
print(nums)

def next_secret(num):
	a = (num ^ (num * 64)) % 16777216
	b = (a ^ (a // 32)) % 16777216
	c = (b ^ (b * 2048)) % 16777216
	return c
	
n = 2000
	
for i in range(2000):
	for j in range(len(nexts)):
		nexts[j] = next_secret(nexts[j])
total = 0		
for j in range(len(nexts)):
	total += nexts[j]
	print(f"{nums[j]}: {nexts[j]}")
print(total)
	
