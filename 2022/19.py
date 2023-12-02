from collections import deque
import re

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
	except EOFError:
		break
		
print(f"{blueprints}")

def can_afford(costs, resources):
	for i in range(len(Blueprint.names)):
		if costs[Blueprint.names[i]] > resources[i]:
			return False
	return True
	
def consum(costs, resources):
	for i in range(len(Blueprint.names)):
		resources[i] -= costs[Blueprint.names[i]]
	return resources
	
STOP = 24

geodes_pb = 0
checked = 0

for bidx, b in enumerate(blueprints):
	q = deque()
	q.append((0, [1, 0, 0, 0], [0, 0, 0, 0], [])) # t, [ore bots, clay bots, obsidian bots, geode bots], [ore, clay, obsidian, geode]

	while len(q) > 0: # dfs
		checked += 1
		t, bots, resources, hist = q.popleft()
		bots = list(bots)
		resources = list(resources)
		hist = list(hist)
		
		if checked % 100000 == 0:
			print(f"checked {checked} paths, blueprint={bidx}, t={t}, bots={bots}, resources={resources}, moves={hist}")
		
		if t >= STOP:
			if resources[3] > geodes_pb:
				print(f"new geodes pb: blueprint={bidx}, t={t}, bots={bots}, resources={resources}, moves={hist}")
				geodes_pb = resources[3]
			continue
		
		# minecraft
		resources2 = list(resources)
		for i in range(len(Blueprint.names)):
			resources2[i] += bots[i]
		
		# see if we can make any constructions
		
		for i, dev in enumerate(Blueprint.names):
			r2 = list(resources)
			h2 = list(hist)
			if can_afford(b.costs[Blueprint.names[i]], resources):
				bots2 = list(bots)
				bots2[i] += 1
				consum(b.costs[Blueprint.names[i]], r2)
				h2.append(f'{t}->{Blueprint.names[i]}')
				q.appendleft((t+1, bots2, resources2, h2))
				
		# if we can afford everything, no sense in skipping a purchase
		if all(can_afford(b.costs[Blueprint.names[i]], resources) for i in range(len(Blueprint.names))):
			continue
		q.appendleft((t+1, bots, resources2, hist))
		
		
