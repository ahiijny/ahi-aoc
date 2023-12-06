seeds = input().split(":")[1].split()
seeds = [int(x.strip()) for x in seeds]
print(f"seeds={seeds}")

orders = {}

while True:
	try:
		line = input()
		if not line.endswith(":"):
			continue
		mail = line.split()[0].split("-")
		source = mail[0]
		dest = mail[2]
		orders[(source, dest)] = []
		while True:
			line = input()
			if not line:
				break
			nums = [int(x) for x in line.split()]
			orders[(source,dest)].append(nums)		
	except EOFError:
		break
		
print(f"orders={orders}")

def lookup(source, dest, src_num):
	for rule in orders[(source,dest)]:
		src_start = rule[1]
		dest_start = rule[0]
		span = rule[2]
		if src_start <= src_num and src_num < src_start + span:
			return dest_start + src_num - src_start
	return src_num
	
path = ["seed", "soil", "fertilizer", "water", "light", "temperature", "humidity", "location"]

seed_to_loc = {}

for seed in seeds:
	a = seed
	for i in range(len(path) - 1):
		a = lookup(path[i], path[i+1], a)
	seed_to_loc[seed] = a
	
print(f"seed_to_loc={seed_to_loc}")

print(f"min loc={min(seed_to_loc.values())}")