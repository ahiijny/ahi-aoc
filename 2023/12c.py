import itertools

springs = []
picross = []

while True:
	try:
		p = input().split()
		nus = '?'.join([p[0]] * 5)
		springs.append(['.'] + list(nus) + ['.']) # add extra
		picross.append([int(d) for d in p[1].split(",")] * 5)
	except EOFError:
		break
		
print(f"springs={springs}")
print(f"picross={picross}")

def validate(s, p):
	on = False
	count = 0
	pi = 0
	if len(p) == 0 and '#' in s:
		return False
		
	for i in range(len(s)):
		if not on:
			if s[i] != '.':
				on = True
				count += 1
		elif on:
			if s[i] == '.':
				on = False
				
				if pi >= len(p):
					return False
				if count != p[pi]:
					return False
				pi += 1				
				count = 0
				
			else:
				count += 1
	if pi < len(p):
		return False
	return True
	
def can_place(s, group_size, left_idx, right_idx):
	# right_idx = location of trailing space
	# e.g. for "##.", group_size=2, then right_idx=2 is a valid placement
	# 0 <= left_idx <= right_idx < len(s)
	
	if right_idx - left_idx < group_size:
		return False
		
	# blanks
	
	for i in range(left_idx, right_idx - group_size):
		if s[i] == '#':
			return False

	# the group
	
	for i in range(right_idx - group_size, right_idx):
		if s[i] == '.':
			return False
			
	# the trailing spacer
	if s[right_idx] == '#':
		return False
	
	return True
		
arrangements = []

for s, p in zip(springs, picross):
	dp = [[0 for i in range(len(s))] for j in range(len(p))]
	print(f"s = {''.join(s)}")
	print(f"\tp = {' '.join([str(pi) for pi in p])}")
	print(f"\tdp: p x s = {len(dp)} x {len(dp[0])}")
	
	# recurrence relation for dp solve
	# dp[pi][si] represents the number of arrangements for the substring of s up to and including character si, for the digits up to and including pi
	# to avoid double counting, the count at dp[pi][si] only includes the arrangements
	# where the group pi ends at index si-1, and the trailing space is at si
	
	# note that because we append a trailing space at the end, we can assume every group will end with a single space	
	
	# example solve:
	#       - | . # # ? ? ? ? ? # # ? ? ? ? ? ? . . 2,2,2,1
	#       2 | 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
	#     2 2 | 0 0 0 0 0 0 1 1 0 1 0 0 0 0 0 0 0 0
	#   2 2 2 | 0 0 0 0 0 0 0 0 0 0 2 0 0 1 1 1 0 0
	# 2 2 2 1 | 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 3 3 0 = 12
	
	# because of padding, can guarantee first and last characters always '.'
	
	for pi in range(len(dp)):
		prevs = [0 for i in range(len(s))]
		prevs[0] = 1
		if pi != 0:
			prevs = dp[pi-1]
		for prev_pi in range(len(prevs)):
			if prevs[prev_pi] != 0:
				for si in range(prev_pi+1, len(s)):
					if can_place(s, p[pi], prev_pi+1, si):
						dp[pi][si] += prevs[prev_pi]
	
	
	if False:
		for pi in dp:
			for si in pi:
				print('{0:<2}'.format(si), end='')
			print()
	
	print(f"\tnum arangements = {sum(dp[-1])}")
	arrangements.append(sum(dp[-1]))
	
print(f"sum = {sum(arrangements)}")



	
	
	

	
	

		
