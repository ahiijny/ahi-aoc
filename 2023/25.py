import networkx as nx
import math

nodes = {}
edges = {}
edge_list = []

while True:
	try:
		line = input().split(':')
		a = line[0]
		bs = [b.strip() for b in line[1].split()]
		nodes[a] = True
		if a not in edges:
			edges[a] = []
		for b in bs:
			nodes[b] = True
			if b not in edges:
				edges[b] = []
			edges[a].append(b)
			edges[b].append(a)
			edge_list.append((a,b))
	except EOFError:
		break
		
#print(f"nodes = {nodes}")
#print(f"edges = {edges}")
		
print(f"num edges = {len(edge_list)}")

# using networkx

G = nx.Graph()

for n in nodes:
	G.add_node(n)

for e in edge_list:
	G.add_edge(*e)
	
print(G)

edge_cut = nx.minimum_edge_cut(G)
print(f'minimum edge cut = {edge_cut}')

for e in edge_cut:
	G.remove_edge(*e)
	
cc = list(nx.connected_components(G))
lcc = list(len(c) for c in cc)

print(f"components: {lcc}")

print(f"product = {math.prod(lcc)}")