import itertools
import functools
import copy

values = {}
inputs = {}
orig_inputs = {}

max_x = 0
max_y = 0
max_z = 0

try:
	while True:
		line = input().split(":")
		if len(line) == 1:
			break
		wire = line[0]
		values[wire] = wire
	while True:
		gate = input().split("->")
		line = [x.strip() for x in gate[0].split()]
		dest = gate[1].strip()
		orig_inputs[dest] = line
		if dest[0] == 'z':
			max_z = max(max_z, int(dest[1:]))
		if dest[0] == 'x':
			max_x = max(max_x, int(dest[1:]))
		if dest[0] == 'z':
			max_y = max(max_y, int(dest[1:]))
except EOFError:
	pass

inputs = dict(orig_inputs)
print(f"initial values: {values}")
print(f"inputs: {inputs}")
print(f"max_z: {max_z}")	

def bin_value(bits_little_endian):
	value = 0
	z = 1
	for b in bits_little_endian:
		value += z * b
		z *= 2
	return value

def calc(wire, values):
	source = inputs[wire]
	if source[0] not in values:
		calc(source[0], values)
	if source[2] not in values:
		calc(source[2], values)
	a = values[source[0]]
	b = values[source[2]]
	if source[1] == 'AND':
		values[wire] = f'({a}) & ({b})'
	elif source[1] == 'OR':
		values[wire] = f'({a}) | ({b})'
	elif source[1] == 'XOR':
		values[wire] = f'({a}) ^ ({b})'

zs = [0] * (max_z+1)

def print_tree(output, level=0):
	if output not in inputs:
		print((" " * level * 2) + f"> " + output)
		return
	print((" " * level * 2) + f"> " + output + ": " + inputs[output][1])
	print_tree(inputs[output][0], level+1)
	print_tree(inputs[output][2], level+1)

@functools.cache
def used_gates(node, nonce=0):
	used = set()
	if node in inputs:
		used.add(node)
		a = inputs[node][0]
		b = inputs[node][2]
		used.update(used_gates(a, nonce))
		used.update(used_gates(b, nonce))
	return used
	
# e.g. if input abc has input x4, x8, y5, return 8
@functools.cache
def highest_gate(node, nonce=0):
	if node not in inputs:
		return int(node[1:])
	return max(highest_gate(inputs[node][0]), highest_gate(inputs[node][2]))

# z0 = x0 ^ y0
# c0 = x0 & y0
# z1 = x1 ^ y1 ^ c0
# c1 = (x1 & y1) | (x1 ^ y1) & c0

def is_z(node, i, nonce=0):
	# return True if node outputs a valid ith z bit, False otherwise
	# to be a valid zi bit, it must be an XOR of xi and yi and c(i-1)
	print(f">is_z({node}, {i}, iteration={nonce}, inputs={inputs[node] if node in inputs else ''})")
	if i == 0:
		return is_x_xor_y(node, i, nonce)
	if i == max_z:
		return is_c(node, i-1, nonce)
	# z1 = x1 ^ x0 ^ c0
	# c0 = x0 & y0
	if inputs[node][1] != 'XOR':
		return False
	if is_x_xor_y(inputs[node][0], i, nonce) and is_c(inputs[node][2], i-1, nonce):
		return True
	if is_x_xor_y(inputs[node][2], i, nonce) and is_c(inputs[node][0], i-1, nonce):
		return True
	return False

@functools.cache
def is_c(node, i, nonce=0):
	print(f">is_c({node}, {i}, iteration={nonce}, inputs={inputs[node] if node in inputs else ''})")
	# return True if node outputs a valid ith carry bit, False otherwise
	# to be a valid ci bit, it must be an OR of (xi AND yi) and (c(i-1) AND (xi XOR yi))
	#print_tree(node)
	if i == 0:
		return is_x_and_y(node, i, nonce)
	if node not in inputs:
		return False
	if inputs[node][1] != 'OR':
		return False
	if is_x_and_y(inputs[node][0], i, nonce) and is_c_clause_2(inputs[node][2], i, nonce):
		return True
	if is_x_and_y(inputs[node][2], i, nonce) and is_c_clause_2(inputs[node][0], i, nonce):
		return True
	return False
	
@functools.cache
def is_x_xor_y(node, i, nonce=0):
	print(f" >is_x_xor_y({node}, {i}, inputs={inputs[node] if node in inputs else ''})")
	ifill = str(i).zfill(2)
	if node not in inputs:
		return False
	return inputs[node][1] == 'XOR' and {inputs[node][0], inputs[node][2]} == {f'x{ifill}', f'y{ifill}'}

@functools.cache
def is_x_and_y(node, i, nonce=0):
	print(f" >is_x_and_y({node}, {i}, inputs={inputs[node] if node in inputs else ''})")
	ifill = str(i).zfill(2)
	if node not in inputs:
		return False
	return inputs[node][1] == 'AND' and {inputs[node][0], inputs[node][2]} == {f'x{ifill}', f'y{ifill}'}

@functools.cache
def is_c_clause_2(node, i, nonce=0):
	print(f">is_c_clause_2({node}, {i}, iteration={nonce}, inputs={inputs[node] if node in inputs else ''})")
	if i == 0:
		raise ValueError("shouldn't happen")
	if node not in inputs:
		return False
	if inputs[node][1] != 'AND':
		return False
	
	if is_c(inputs[node][0], i-1, nonce) and is_x_xor_y(inputs[node][2], i, nonce):
		return True
	if is_c(inputs[node][2], i-1, nonce) and is_x_xor_y(inputs[node][0], i, nonce):
		return True
	return False

nonce = 0 # number of attempts
used = set()
all_gates = set(inputs.keys())

max_pairs = 4

def make_valid(used, i, w, ui, nonce, max_pairs):
	print(f"make_valid: w={w}, nonce={nonce}, max_pairs={max_pairs}")
	orig_nonce = nonce
	global inputs
	global orig_inputs
	sus_gates = ui - used
	swappable_gates = all_gates - used
	# shortcut calculation: e.g. z5 input should not receive inputs from x10
	swappable_gates = set([sg for sg in swappable_gates if highest_gate(sg, orig_nonce) <= i])
	print(f"number of sus gates: {len(sus_gates)}")
	
	for num_pairs in range(1, min(max_pairs, len(sus_gates)) + 1):
		for sus_gate_choose in itertools.combinations(sus_gates, num_pairs):
			# there will be some repeats but whatevs
			target_gates = swappable_gates - set(sus_gate_choose)
			
			# find all possible ways of swapping sus (A, B) <-> target (C, D, E, F)
			# e.g. for A-C B-D, A-C B-E, etc.
			print(f"checking swaps for {sus_gate_choose}, num_target_gates={len(target_gates)}, nonce={nonce}")
			
			for target_gate_choose in itertools.combinations(target_gates, len(sus_gate_choose)):
				
				checked_swaps = set()
				
				for target_gate_perm in itertools.permutations(target_gate_choose, len(sus_gate_choose)):
					# swap sus_gate_choose[i] with target_gate_perm[i]
					
					swap_key = frozenset([tuple(sorted((sus_gate_choose[i], target_gate_perm[i]))) for i in range(num_pairs)])
					if swap_key in checked_swaps:
						continue
					print(f"checking swap: {swap_key}")						
					inputs = copy.deepcopy(orig_inputs)
					nonce += 1
					for swap in swap_key:
						inputs[swap[0]], inputs[swap[1]] = inputs[swap[1]], inputs[swap[0]]
					valid = is_z(w, i, nonce)
					if valid:
						print(f"...swap is valid!!!: {swap_key}")
						orig_inputs = inputs
						return nonce, swap_key
					checked_swaps.add(swap_key)
					
	raise ValueError("it's joever... no swaps make it valid")
all_swaps = set()

for i in range(max_z + 1):
	w = 'z' + str(i).zfill(2)
	ui = used_gates(w, nonce)
	calc(w, values)
	#print_tree(w)
	print(f"checking {w}")
	valid = is_z(w, i, nonce)
	print(f"... valid={valid}")
	# if not valid, randomly swap affected gates until it becomes valid
	if not valid:
		nonce, swaps = make_valid(used, i, w, ui, nonce, max_pairs)
		all_swaps.update(swaps)
		max_pairs -= len(swaps)
	used.update(ui)
		
print(f"all_swaps: {all_swaps}")

changed_nodes = []
for swap in all_swaps:
	changed_nodes.append(swap[0])
	changed_nodes.append(swap[1])
print(",".join(sorted(changed_nodes)))
		

	

#for w in inputs:
#	if w[0] == 'z':
#		calc(w, values)
#		idx = int(w[1:])
#		zs[idx] = values[w]

#for w in sorted(values.keys()):
#	if w[0] == 'z':
#		print(f"{w}: {values[w]}")

