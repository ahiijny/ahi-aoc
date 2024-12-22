from collections import deque

nums = []
deltas = []
nexts = []

try:
	while True:
		nums.append(int(input()))
except EOFError:
	pass
nexts = list(nums)	
deltas = [[] for j in range(len(nexts))]
print(nums)

def next_secret(num):
	a = (num ^ (num * 64)) % 16777216
	b = (a ^ (a // 32)) % 16777216
	c = (b ^ (b * 2048)) % 16777216
	return c
	
n = 2000

delta_prices = [{} for j in range(len(nexts))]
	
for j in range(len(nexts)):
	print(f"j={j}, dcache sizes={[len(x) for x in delta_prices]}")
	for i in range(2000):
		n = next_secret(nexts[j])
		d = n % 10 - nexts[j] % 10
		deltas[j].append(d)
		nexts[j] = n
		if len(deltas[j]) >= 4:
			d4 = ''.join(str(x) for x in deltas[j][-4:])
			if d4 not in delta_prices[j]:
				delta_prices[j][d4] = nexts[j] % 10
			del deltas[j][0]

# find best deltas
best_delta = None
best_price = None

for j in range(len(delta_prices)):
	print(f"j={j}")
	for d in delta_prices[j]:
		price = sum(delta_prices[k].get(d, 0) for k in range(len(delta_prices)))
		if best_price is None or best_price < price:
			best_delta = d
			best_price = price
			print(f"...found improvement: delta={best_delta}, price={best_price}")
print(f"best price: {best_price}")
