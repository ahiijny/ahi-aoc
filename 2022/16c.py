from collections import deque
import random
import itertools

all_nodes = {}
dist = {}
vip = set()

while True:
	try:
		line = input().split()
		if len(line) == 0:
			break
		name = line[1]
		rate = int(line[4].split('=')[1].replace(';', ''))
		nb = [n.replace(',', '') for n in line[9:]]
		all_nodes[name] = (rate, nb)
		if rate > 0:
			vip.add(name)
	except EOFError:
		break
		
print(f"nodes: {all_nodes}")
print(f"vip nodes: {vip}")

def dist_calc(nodes, dist):
	for start in nodes:
		dist[start] = {}
		dist[start][start] = (0, [])
		
		qq = deque()
		qq.append((start, []))
		visited = set()
		
		while len(visited) < len(nodes):
			n, path = qq.popleft()
			path = list(path)
			
			visited.add(n)
			nb = nodes[n][1]
			
			for n2 in nb:
				if n2 in visited:
					continue
				path2 = path + [n2]
				if n2 not in dist[start]:
					dist[start][n2] = (len(path2), path2)					
				visited.add(n2)
				qq.append((n2, path2)) # bfs
				
dist_calc(all_nodes, dist)
print(f"optimal routes: {dist}")

TOTAL_TIME = 26
t = 0
best_press = 0
checked = 0
routes_checked = 0

# find optimals for every subset pairing

def get_subset_pairs(vips):
	pairs = []
	for n in range(0, len(vips)//2+1):
		for c in itertools.combinations(vips, n):
			pairs.append((set(c), vips - set(c)))
	return pairs
	
pairs = get_subset_pairs(vip)

print(f"number of partitions between two actors: {len(pairs)}")

def calc_potential_remaining_press(t, dist, candidates):
	global all_nodes
	global TOTAL_TIME
	remaining = 0
	for n in candidates:
		rate, nb = all_nodes[n]
		remaining += (TOTAL_TIME - (t + 1)) * rate
	return remaining

for pidx, vip_pair in enumerate(pairs):
	best_presses = [0, 0]
	best_paths = [[], []]
	for vidx, vip in enumerate(vip_pair):
		q = deque()
		q.append((0, 'AA', set(), 0, [])) # current node, set of open valves, total pressure, time
		while len(q) > 0:
			checked += 1
			t, node, valves, press, path = q.popleft()
			valves = set(valves)
			path = list(path)
			
			rate, nb = all_nodes[node] # options are to either open valve, or move to neighbouring valve
			
			if t >= TOTAL_TIME:
				if press > best_presses[vidx]:
					# print(f"..new pb: press={press}, path={path}, valves={valves}, pidx={pidx}, pair={vip_pair}, routes_checked={routes_checked}")
					best_presses[vidx] = press
					best_paths[vidx] = path
				routes_checked += 1
				continue
			
			# get distances to neighbouring vip and not opened valves
			candidates = vip - valves - {node}
				
			if node not in valves and rate > 0: # only worth opening if rate > 0
				# open valve
				t2 = t+1
				valves2 = valves.union({node})
				press2 = press + (TOTAL_TIME - t2) * rate
				path2 = path + ['>' + node]
				ceiling = calc_potential_remaining_press(t2, dist, candidates)
				if press2 + ceiling < best_presses[vidx]: # no point if queueing if there's no way we can catch up
					continue
				q.appendleft((t2, node, valves2, press2, path2))
				
				if len(path) > 0:
					continue # we are only queueing trips to valves to open them, so aside from the first node, we can ignore the possibility of not opening nodes
				
			# sort in descending order so that nearest one is visited first
			neighbours = sorted([(dist[node][n], n) for n in candidates], reverse=True)
			
			if len(neighbours) == 0: # no more valves to open, just chill for the rest of the session
				q.appendleft((TOTAL_TIME, node, valves, press, path))
			
			if checked % 1000000 == 0:
				print(f"currently checking: t={t}, node={node}, valves={valves}, press={press}, path={path}, best_press={best_press}, candidates={candidates}, neighbours={neighbours}")
			for (d, p), n in neighbours:
				t2 = t + len(p)
				path2 = path + p
				ceiling = calc_potential_remaining_press(t2, dist, candidates)
				if press + ceiling < best_presses[vidx]: # no point if queueing if there's no way we can catch up
					continue
				q.appendleft((t2, n, valves, press, path2))
	total_press = sum(best_presses)
	if total_press > best_press:
		print(f"!!! new pb: press = {total_press}, best_paths = {best_paths}, paritions searched = {pidx}")
		best_press = total_press
