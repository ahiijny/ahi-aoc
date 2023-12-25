from enum import Enum
from copy import deepcopy
from collections import deque

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
		else:
			state[name] = {} # inputs with high pulses
		for dest in d: # cover untyped modules
			if dest not in types:
				types[dest] = None
				dests[dest] = []
				types[dest] = None
		
	except EOFError:
		break
		

for name in dests:
	for dest in dests[name]:
		if types[dest] == '&':
			state[dest][name] = False # record conjunction state inputs

print(f"dests={dests}, types={types}, state={state}")

# repeats

N = 1000

# False = low, True = high
pulse_counts = [0, 0]
q = deque()

for i in range(N):
	q.appendleft(('button', 'broadcaster', False)) 
	pulse_counts[0] += 1
	
	while len(q) > 0:
		source, module, pulse = q.popleft()
		#print(f"{source} -> {module}: {1 if pulse else 0}")
		if types[module] == '':
			for dest in dests[module]:
				pulse_counts[int(pulse)] += 1
				pnext = pulse
				q.append((module, dest, pnext))
		elif types[module] == '%': # flipflop		
			if pulse == False:
				state[module] = not state[module]
				pnext = state[module]
				for dest in dests[module]:
					pulse_counts[int(pnext)] += 1
					q.append((module, dest, pnext))
		elif types[module] == '&': # conjunction
			if pulse == True:
				state[module][source] = True
			else:
				state[module][source] = False
			pnext = not all(state[module].values())
			for dest in dests[module]:
				pulse_counts[int(pnext)] += 1
				q.append((module, dest, pnext))

print(f"low pulses = {pulse_counts[0]}, high pulses = {pulse_counts[1]}")
print(f"product = {pulse_counts[0] * pulse_counts[1]}")