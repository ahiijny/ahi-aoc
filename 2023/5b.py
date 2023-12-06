from collections import deque

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
		
for k in orders:
	orders[k] = sorted(orders[k], key=lambda o: o[1])

print(f"orders={orders}")

seed_ranges = [] # [start, end) intervals

for i in range(0, len(seeds), 2):
	seed_ranges.append((seeds[i], seeds[i] + seeds[i+1]))
	
print(f"seed_ranges={seed_ranges}")

def split(r, at):
	return [(r[0], at), (at, r[1])]

def lookup(source, dest, src_ranges):
	# print(f"{source}->{dest}:")
	# print(f"\t{src_ranges}")
	dest_ranges = set()
	for sr in src_ranges:
		sr_pieces = deque([sr])
		# cut pieces
		for rule in orders[(source,dest)]: # note: rules will be sorted in ascending order by location. so only need to worry about trailing halves
			next_sr_pieces = deque()
			while len(sr_pieces) > 0:
				sr = sr_pieces.popleft()
				s1 = sr[0]
				s2 = sr[1]
				rs1 = rule[1]
				rd1 = rule[0]
				span = rule[2]
				rs2 = rs1 + span
				rd2 = rd1 + span
				
				# s1   s2
				# x----o
				#    x------o
				#    rs1    rs2
				#                       x------o
				#                      rd1     rd2
				# print(f".....s={sr},rs=({rs1},{rs2}),rd=({rd1},{rd2})")
				if s2 <= rs1:
					dest_ranges.add(sr)
				elif s1 >= rs2:
					next_sr_pieces.append(sr)
				elif s1 < rs1 and s2 <= rs2:
					dest_ranges.add((s1, rs1))
					dest_ranges.add((rd1, rd1 + (s2-rs1)))
				elif s1 < rs1 and s2 > rs2:
					dest_ranges.add((s1, rs1))
					dest_ranges.add((rd1, rd2))
					next_sr_pieces.append((rs2, s2))
				elif s1 >= rs1 and s2 <= rs2:
					dest_ranges.add((rd1 + (s1-rs1), rd1 + (s2-rs1)))
				elif s1 >= rs1 and s2 > rs2:
					dest_ranges.add((rd1 + (s1-rs1), rd2))
					next_sr_pieces.append((rs2, s2))
				# print(f".....next_sr_pieces={next_sr_pieces}, dest_ranges={dest_ranges}")
			sr_pieces = next_sr_pieces
		if len(next_sr_pieces) > 0:
			dest_ranges.update(next_sr_pieces)
	dest_ranges = list(dest_ranges)
	# print(f"\t=> {dest_ranges}")	
	return dest_ranges
	
path = ["seed", "soil", "fertilizer", "water", "light", "temperature", "humidity", "location"]

seed_to_loc = {}

a = seed_ranges

for i in range(len(path) - 1):
	a = lookup(path[i], path[i+1], a)
location_ranges = sorted(a)

print(f"min loc range={location_ranges[0]}")