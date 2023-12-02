from collections import deque
import random

best = {} # best[(node, valves)], defaulting to 0 if not present

all_nodes = {}
dist = {}
vip = set()
q = deque()
q.append(([0, 0], ['AA', 'AA'], set(), 0, [[],[]])) # current node, set of open valves, total pressure, time

def hashs(s):
	return ','.join(sorted(list(s)))

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

def calc_potential_remaining_press(ts, dist, candidates):
	global all_nodes
	global TOTAL_TIME
	remaining = 0
	mint = min(ts)
	for n in candidates:
		rate, nb = all_nodes[n]
		remaining += (TOTAL_TIME - (mint + 1)) * rate
	return remaining
		
	

while len(q) > 0:
	checked += 1
	ts, nodes, valves, press, paths = q.popleft()
	ts = list(ts)
	nodes = list(nodes)
	valves = set(valves)
	paths = list(paths)
	
	if ts[0] >= TOTAL_TIME and ts[1] >= TOTAL_TIME:
		if press > best_press:
			print(f"new pb: press={press}, paths={paths}, valves={valves}, routes_checked={routes_checked}")
			best_press = press
		routes_checked += 1
		continue
		
	# only queue the actor with the smaller time signature
	
	actors = []
	
	if len(vip - valves) == 1: # might need to tiebreak
		actors = [0, 1]
	elif ts[0] < ts[1]:
		actors = [0]
	else:
		actors = [1]
		
	for i in actors:
		node = nodes[i]
		rate, nb = all_nodes[node] # options are to either open valve, or move to neighbouring valve
		
		# get distances to neighbouring vip and not opened valves
		candidates = vip - valves - {node}
		
		
		if node not in valves and rate > 0: # only worth opening if rate > 0
			ts2 = list(ts)
			nodes2 = list(nodes)
			paths2 = list(paths)
			
			# open valve
			ts2[i] = ts[i]+1
			valves2 = valves.union({node})
			press2 = press + (TOTAL_TIME - ts2[i]) * rate
			paths2[i] = paths[i] + ['>' + node]
			ceiling = calc_potential_remaining_press(ts2, dist, candidates)
			if press2 + ceiling < best_press: # no point if queueing if there's no way we can catch up
				continue
			q.appendleft((ts2, nodes2, valves2, press2, paths2))
	
		if len(paths[i]) > 0 and node not in valves:
			# note: after the start, we are only travelling to nodes to open them
			# so, we should not ever travel to a node and not open it
			# so if a traveller is at a node and it is still open, we should not queue
			# trips to other nodes, if it is not the first node
			continue
		
		# sort in descending order so that nearest one is visited first
		neighbours = sorted([(dist[node][n], n) for n in candidates], reverse=True)
		
		if len(neighbours) == 0: # no more valves to open, just chill for the rest of the session
			ts2 = list(ts)
			ts2[i] = TOTAL_TIME
			q.appendleft((ts2, nodes, valves, press, paths))
			continue
		
		if checked % 1000000 == 0:
			print(f"currently checking: press={press}, ts={ts}, nodes={nodes}, valves={valves}, paths={paths}, best_press={best_press}, candidates={candidates}, neighbours={neighbours}")
			
		for (d, p), n in neighbours:
			ts2 = list(ts)
			nodes2 = list(nodes)
			nodes2[i] = n
			paths2 = list(paths)
			ts2[i] = ts[i] + len(p)
			paths2[i] = paths[i] + p
			ceiling = calc_potential_remaining_press(ts2, dist, candidates)
			if press + ceiling < best_press: # no point if queueing if there's no way we can catch up
				continue
			q.appendleft((ts2, nodes2, valves, press, paths2))
