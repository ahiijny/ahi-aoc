from collections import deque

best = {} # best[(node, valves)], defaulting to 0 if not present

nodes = {}
dist = {}
vip = set()
q = deque()
q.append((0, 'AA', set(), 0, [])) # current node, set of open valves, total pressure, time

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
		nodes[name] = (rate, nb)
		if rate > 0:
			vip.add(name)
	except EOFError:
		break
		
print(f"nodes: {nodes}")
print(f"vip nodes: {vip}")

def dist_calc(nodes, dist):
	for start in nodes:
		dist[start] = {}
		
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
				
dist_calc(nodes, dist)
print(f"optimal routes: {dist}")

TOTAL_TIME = 30
t = 0
best_press = 0
checked = 0
routes_checked = 0

seen = set()

while len(q) > 0:
	checked += 1
	t, node, valves, press, path = q.popleft()
	#seen.add((t, node, ','.join(sorted(list(valves))), press))
	valves = set(valves)
	path = list(path)
	
	rate, nb = nodes[node] # options are to either open valve, or move to neighbouring valve
	
	if t >= 30:
		if press > best_press:
			print(f"new pb: path={path}, valves={valves}, press={press}, routes_checked={routes_checked}")
			best_press = press
		routes_checked += 1
		if routes_checked > 720:
			#break
			pass
		continue
		
	if node not in valves and rate > 0: # only worth opening if rate > 0
		# open valve
		t2 = t+1
		valves2 = valves.union({node})
		press2 = press + (TOTAL_TIME - t2) * rate
		path2 = path + ['>' + node]
		#if (t2, node, ','.join(sorted(list(valves2))), press2) in seen:
			#print(f"seen already!: {(t2, n, ','.join(sorted(list(valves))), press)}")
			#continue
		q.appendleft((t2, node, valves2, press2, path2))
		#seen.add((t2, node, ','.join(sorted(list(valves2))), press2))
		
		if len(path) > 0:
			continue # we are only queueing trips to valves to open them, so aside from the first node, we can ignore the possibility of not opening nodes
		
	# get distances to neighbouring vip and not opened valves
	candidates = vip - valves - {node}
	
	# sort in descending order so that nearest one is visited first
	neighbours = sorted([(dist[node][n], n) for n in candidates], reverse=True)
	
	if len(neighbours) == 0: # no more valves to open, just chill for the rest of the session
		q.appendleft((30, n, valves, press, path))
	
	if checked % 1000000 == 0:
		pass
		print(f"currently checking: t={t}, node={node}, valves={valves}, press={press}, path={path}, best_press={best_press}, candidates={candidates}, neighbours={neighbours}")
	for (d, p), n in neighbours:
		t2 = t + len(p)
		path2 = path + p
		#if (t2, n, ','.join(sorted(list(valves))), press) in seen:
			#print(f"seen already!: {(t2, n, ','.join(sorted(list(valves))), press)}")
			#continue
		q.appendleft((t2, n, valves, press, path2))
		#seen.add((t2, n, ','.join(sorted(list(valves))), press))
		
	
	