import math
from enum import Enum
from copy import deepcopy
from collections import deque
import ast

dests = {}
types = {}
state = {}

while True:
	try:
		line = input().split('->')
		name = line[0].strip()
		if name[0] == '%' or name[0] == '&': # flipflop or conjunction
			kind = name[0]
			name = name[1:]			
		else:
			kind = '' # broadcaster
		d = [x.strip() for x in line[1].split(',')]
		dests[name] = d
		types[name] = kind
		if kind == '%':
			state[name] = False
		elif kind == '&':
			state[name] = {} # inputs with multiple inputs
		else:
			state[name] = None
		for dest in d: # cover untyped modules
			if dest not in types:
				types[dest] = None
				dests[dest] = []
				types[dest] = None
			if dest not in state:
				state[dest] = None
	except EOFError:
		break
		

for name in dests:
	for dest in dests[name]:
		if types[dest] == '&':
			state[dest][name] = False # record conjunction state inputs

print(f"dests={dests}\n\ttypes={types}\n\tstate={state}")

def subtree(state, keys):
	sub = {k: state[k] for k in keys}
	return sub
	
def calc_lcm(state_hist, state_loops, poi, ons):
	"""
		e.g.  ons = {'mf': 3761, 'fz': 3793, 'fh': 3847, 'ss': 3881}
		which means during the nth button press, it sends a 1 signal
		they all loop from (1, n), so after the lcm, which means 
		state 1=n
		loop duration = (n-1)
		
		equivalent state = i % (n-1)
		
		e.g. n = 17
		1 2 3 4... 17 18
		17 -> 1
		17 % 16 = 1
		18 % 16 = 2
	"""
	
	print(f"ons: {ons}")
	
	reverse = {}
	values = []
	
	for p in poi:
		reverse[p] = {}
		
		for st, i in state_hist[p].items():
			#print(f"parsing: {st}")
			st = ast.literal_eval(st)
			reverse[p][i] = st
			
	for p in poi:
		print(f"{p}: loop = {state_loops[p]}")
		values.append(state_loops[p][1]-1)
		for i in range(len(reverse[p])):
			st = reverse[p][i]
			value = st[p]
			on = not all(value.values())
			#print(f"  {1 if on else 0}", end='')
		print()
	print(f"lcm: {math.lcm(*values)}")

def sort_d(d):
	res = {}
	for k,v in sorted(d.items()):
		if isinstance(v, dict):
			res[k] = sort_d(v)
		else:
			res[k] = v
	return res
	
def stringify(d):
	return str(sort_d(d))
	
def calc_affected_by():
	affected_by = {}
	for name in dests:
		affected_by[name] = set()
		
	for name in dests:
		visited = {name: True}
		# start at node and walk until all nodes visited or roads run out
		q = deque()
		q.appendleft(name)
		while len(q) > 0:
			n = q.popleft()
			visited[n] = True
			for d in dests[n]:
				if d in visited:
					continue
				q.appendleft(d)
		print(f"nodes reachable from {name}: {list(visited)}")
		for v in visited:
			affected_by[v].add(name)
	
	return affected_by

def walk(N, state, affected_by, poi=[], should_calc_lcm=False):
	# False = low, True = high
	pulse_counts = [0, 0]
	q = deque()
	ons = {} # simplifying assumption: only 1 on send per poi

	i = 0

	done = False
	
	state_hist = {} # state_hist[module][stringify(state)] = index number
	state_loops = {}
	for name in dests:
		state_hist[name] = {}
		
	for name in dests:		
		state_hist[name][stringify(subtree(state,affected_by[name]))] = 0

	while not done:
		i += 1
		if i % 1000 == 0:
			print(f"tested {i} button presses")
		q.appendleft(('button', 'broadcaster', False, ['broadcaster'])) 
		pulse_counts[0] += 1
		
		while len(q) > 0:
			source, module, pulse, path = q.popleft()
			if source in poi and pulse:
				print(f"{source}->{module}: {1 if pulse else 0}, state={state[source]}")
				ons[source] = i
			if module == 'rx' and pulse == False:
				print(f'False state received at rx after {i} button presses')
				done = True
			#print(f"{source} -> {module}: {1 if pulse else 0}")
			if types[module] == '':
				for dest in dests[module]:
					pulse_counts[int(pulse)] += 1
					pnext = pulse
					q.append((module, dest, pnext, path + [dest]))
			elif types[module] == '%': # flipflop		
				if pulse == False:
					state[module] = not state[module]
					pnext = state[module]
					for dest in dests[module]:
						pulse_counts[int(pnext)] += 1
						q.append((module, dest, pnext, path + [dest]))
			elif types[module] == '&': # conjunction
				if pulse == True:
					state[module][source] = True
				else:
					state[module][source] = False
				pnext = not all(state[module].values())
				for dest in dests[module]:
					pulse_counts[int(pnext)] += 1
					q.append((module, dest, pnext, path + [dest]))
		
		for name in affected_by:
			if name in state_loops:
				continue
			new_state = stringify(subtree(state,affected_by[name]))
			if new_state in state_hist[name]:
				old_i = state_hist[name][new_state]
				print(f"found recurring state for module {name}: i={old_i} -> {i}")
				state_loops[name] = (old_i, i)
			else:
				state_hist[name][new_state] = i
		#print(f"i={i}, state={state}")
		if i >= N:
			break
		if all(p in state_loops for p in poi):
			done = True

	print(f"low pulses = {pulse_counts[0]}, high pulses = {pulse_counts[1]}")
	
	if should_calc_lcm:
		calc_lcm(state_hist, state_loops, poi, ons)
	return affected_by
	
# dry run to get affected by graph

poi = ['fh', 'mf', 'fz', 'ss']

affected_by = calc_affected_by()
print(f"\taffected_by={affected_by}")
walk(4000, state, affected_by, poi, True)