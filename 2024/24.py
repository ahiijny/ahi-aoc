values = {}
inputs = {}

max_z = 0

try:
	while True:
		line = input().split(":")
		if len(line) == 1:
			break
		wire = line[0]
		value = int(line[1])
		values[wire] = value
	while True:
		gate = input().split("->")
		line = [x.strip() for x in gate[0].split()]
		dest = gate[1].strip()
		inputs[dest] = line
		if dest[0] == 'z':
			max_z = max(max_z, int(dest[1:]))
except EOFError:
	pass
	
print(f"initial values: {values}")
print(f"inputs: {inputs}")
print(f"max_z: {max_z}")
def calc(wire):
	source = inputs[wire]
	if source[0] not in values:
		calc(source[0])
	if source[2] not in values:
		calc(source[2])
	a = values[source[0]]
	b = values[source[2]]
	if source[1] == 'AND':
		values[wire] = a & b
	elif source[1] == 'OR':
		values[wire] = a | b
	elif source[1] == 'XOR':
		values[wire] = a ^ b		
zs = [0] * (max_z+1)

for w in inputs:
	calc(w)
	if w[0] == 'z':
		idx = int(w[1:])
		zs[idx] = values[w]

def bin_value(bits_little_endian):
	value = 0
	z = 1
	for b in bits_little_endian:
		value += z * b
		z *= 2
	return value
	
for w in sorted(values.keys()):
	print(f"{w}: {values[w]}")
print(f"zs: {zs}")
print(f"value: {bin_value(zs)}")
		


