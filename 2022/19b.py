from collections import deque
import re
import math

class Blueprint:	
	names = ['ore', 'clay', 'obsidian', 'geode']
	def __init__(self):	
		self.costs = {
			'ore': {},
			'clay': {},
			'obsidian': {},
			'geode': {}
		}
		
		for cost in self.costs:
			for name in Blueprint.names:
				self.costs[cost][name] = 0
		
		self.counts = {
			'ore': 1,
			'clay': 0,
			'obsidian': 0,
			'geode': 0
		}
		
	def parse(self, data):
		indata = iter(data)
		
		n = next(indata)
		self.num = int(n.split()[1].replace(':',''))
		self.costs['ore']['ore'] = int(next(indata).strip().split()[4])
		self.costs['clay']['ore'] = int(next(indata).strip().split()[4])
		
		l = next(indata).strip().split()
		self.costs['obsidian']['ore'] = int(l[4])
		self.costs['obsidian']['clay'] = int(l[7])
		
		l = next(indata).strip().split()
		self.costs['geode']['ore'] = int(l[4])
		self.costs['geode']['obsidian'] = int(l[7])
		
	def __repr__(self):
		return str(self)
		
	def __str__(self):
		return f'blueprint {self.num}: ' + str(self.costs)

blueprints = []

while True:
	try:
		data = input()
		if len(data.strip()) == 0:
			break
		data = re.split('\.|:', data)
		b = Blueprint()
		b.parse(data)
		blueprints.append(b)
		if len(blueprints) == 3:
			break
	except EOFError:
		break
		
print(f"{blueprints}")

def can_afford(costs, resources):
	for i in range(len(Blueprint.names)):
		if costs[Blueprint.names[i]] > resources[i]:
			return False
	return True
	
def consum(costs, resources):
	# print(f"consum: {resources} - {costs}", end="")
	for i in range(len(Blueprint.names)):
		resources[i] -= costs[Blueprint.names[i]]
	if any(k < 0 for k in resources):
		print(f"consum: {costs} -> {resources}")
	return resources
	
def how_long_wait(blueprint, bots, resources, i):
	costs = [blueprint.costs[Blueprint.names[i]][Blueprint.names[j]] for j in range(len(Blueprint.names))]
	waits = []
	
	for j in range(len(Blueprint.names)):
		if costs[j] <= resources[j]:
			waits.append(0)
		elif bots[j] == 0:
			return -1
		else:
			waits.append(int(math.ceil((costs[j] - resources[j]) / bots[j])))	
	return max(waits)
	
STOP = 32
checked = 0

def calc_ceiling(blueprint, t, bots, resources, geodes_pb):
	dt = STOP - t
	confirmed = resources[3] + bots[3] * dt
	ceiling = 0
	for t2 in range(t+1, STOP):
		ceiling += STOP - t2
	return confirmed + ceiling
	
	

def get_future(bots, resources, deltat):
	resources2 = list(resources)
	for i in range(len(Blueprint.names)):
		resources2[i] += deltat * bots[i]
	return resources2

pbs = []

for bidx, b in enumerate(blueprints):
	print(f">>> BLUEPRINT {bidx}")
	geodes_pb = 0
	q = deque()
	q.append((0, [1, 0, 0, 0], [0, 0, 0, 0], [])) # t, [ore bots, clay bots, obsidian bots, geode bots], [ore, clay, obsidian, geode]

	while len(q) > 0: # dfs
		checked += 1
		t, bots, resources, hist = q.popleft()
		bots = list(bots)
		resources = list(resources)
		hist = list(hist)
		
		#if checked > 60:
			#break
		
		if calc_ceiling(b, t, bots, resources, geodes_pb) < geodes_pb: # prune
			continue
		
		if checked % 5000000 == 0:
			print(f"checked {checked} paths, blueprint={bidx}, t={t}, bots={bots}, resources={resources}, moves={hist}")
		
		if t == STOP:
			if resources[3] > geodes_pb:
				print(f" blueprint={bidx}: new geodes pb: {resources[3]}, t={t}, bots={bots}, resources={resources}, moves={hist}")
				geodes_pb = resources[3]
			continue
		
		# see if we can make any constructions
		qcount = 0
		
		for i, dev in enumerate(Blueprint.names):
			r2 = list(resources)
			h2 = list(hist)
			wait = how_long_wait(b, bots, resources, i)
			if wait != -1:
				qcount += 1
				t2 = t + wait + 1
				if t2 > STOP:
					continue
				bots2 = list(bots)
				bots2[i] += 1
				r2 = get_future(bots, resources, wait+1)
				consum(b.costs[Blueprint.names[i]], r2)
				h2.append(f'{t+wait}->{Blueprint.names[i]}')
				
				if calc_ceiling(b, t2, bots2, r2, geodes_pb) < geodes_pb: # prune
					continue
				q.appendleft((t2, bots2, r2, h2))		

		if qcount == 0:
			q.appendleft((STOP, bots, get_future(bots, resources, STOP-t, hist)))
	
	pbs.append(geodes_pb)
	
print(f"geode pbs: {pbs}")

product = 1
for pb in pbs:
	product *= pb
	
print(f"product of top 3: {product}")
