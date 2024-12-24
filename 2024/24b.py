values = {}
inputs = {}

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
		inputs[dest] = line
		if dest[0] == 'z':
			max_z = max(max_z, int(dest[1:]))
		if dest[0] == 'x':
			max_x = max(max_x, int(dest[1:]))
		if dest[0] == 'z':
			max_y = max(max_y, int(dest[1:]))
except EOFError:
	pass
	
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

for w in inputs:
	if w[0] == 'z':
		calc(w, values)
		idx = int(w[1:])
		zs[idx] = values[w]

for w in sorted(values.keys()):
	if w[0] == 'z':
		print(f"{w}: {values[w]}")

