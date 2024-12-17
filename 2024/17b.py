import itertools

class Code:
	def __init__(self):	
		self.a = int(input().split(":")[1])
		self.b = int(input().split(":")[1])
		self.c = int(input().split(":")[1])
		input()
		self.p = [int(x) for x in input().split(":")[1].split(",")]
			
		print(f"a={self.a}")
		print(f"b={self.b}")
		print(f"c={self.c}")
		print(f"p={self.p}")

		self.i = 0
		self.stdout = []
		
	def op(self, x):
		if 0 <= x and x <= 3:
			return x
		if x == 4:
			return self.a
		elif x == 5:
			return self.b
		elif x == 6:
			return self.c
		elif x == 7:
			raise ValueError("invalid")

	def adv(self, x):
		#print(f">adv {x}")
		x = self.op(x)
		self.a = self.a // (2 ** x)
		self.i += 2
		
	def bxl(self, x):
		#print(f">bxl {x}")
		self.b = self.b ^ x
		self.i += 2
		
	def bst(self, x):
		#print(f">bst {x}")
		x = self.op(x)
		self.b = x % 8
		self.i += 2
		
	def jnz(self, x):
		#print(f">jnz {x}")
		if self.a == 0:
			self.i += 2
			return
		self.i = x
		
	def bxc(self, x):
		#print(f">bxc {x}")
		self.b = self.b ^ self.c
		self.i += 2
		
	def out(self, x):
		#print(f">out {x}")
		x = self.op(x)
		self.stdout.append(x % 8)
		self.i += 2
		
	def bdv(self, x):
		#print(f">bdv {x}")
		x = self.op(x)
		self.b = self.a // (2 ** x)
		self.i += 2
		
	def cdv(self, x):
		#print(f">cdv {x}")
		x = self.op(x)
		self.c = self.a // (2 ** x)
		self.i += 2
		
	def run(self):
		f = {
			0: self.adv,
			1: self.bxl,
			2: self.bst,
			3: self.jnz,
			4: self.bxc,
			5: self.out,
			6: self.bdv,
			7: self.cdv
		}
		self.i = 0
		self.b = 0
		self.c = 0
		self.stdout = []
		while self.i < len(self.p):
			#print(f"i={self.i}")
			opcode = self.p[self.i]
			operand = self.p[self.i+1]
			f[opcode](operand)
			
		#print(",".join([str(x) for x in self.stdout]))
		
c = Code()
c.run()

"""
 2,4: B <- [A] % 8				store A lowest 3 bits into B
 1,3: B <- [B] XOR 0b11         if <= 3, subtract from 3, else subtract from 11, store into B
 7,5: C <- [A] >> [B]			rightshift A by B, store into C
 0,3: A <- [A] >> 3				rightshift A by 3, store into A
 1,4: B <- [B] XOR 0b100		
 4,7: B <- [B] XOR [C]
 5,5: out << [B] % 8
 3,0: JUMP 0 if [A] != 0
 
   XOR          XOR
000 011  = 011  100 = 111
001 011  = 010  100 = 110
010 011  = 001  100 = 101
011 011  = 000  100 = 100
100 011  = 111  100 = 000
101 011  = 110  100 = 001
110 011  = 101  100 = 010
111 011  = 100  100 = 011

0 -> 3
1 -> 2
2 -> 1
3 -> 0
4 -> 7 -1
5 -> 6 -2
6 -> 5 -3
7 -> 4 -4


0 -> 4
1 -> 5
2 -> 6
3 -> 7
4 -> 0
5 -> 1
6 -> 2
7 -> 3


output = (~b[0:2] XOR (b[0:2] >> b[0:2] XOR 0b11)) % 8

rightshift offsets:
b[0:2]
0 -> 3
1 -> 2
2 -> 1
3 -> 0
4 -> 7
5 -> 6
6 -> 5
7 -> 4


B XOR 3 = 
 
 
 2 << [B] % 8
 
"""

outputs = {}

for a in range(1024):
	# maximum rightshift is 7, plus 3 primary bits, so 10 different bits to search through
	c.a = a
	c.run()
	outputs[a] = list(c.stdout)
	
#print(f"outputs={outputs}")

# search space

q = []
q.append((0, 0, 0)) # little endian binary value

best = None
best_so_far = -1
count = 0
while len(q) > 0:
	a, mask, pi = q.pop()
	count += 1
	if pi > best_so_far or count % 100000 == 0:
		print(f"checking a=0b{a:8b}, pi={pi}, checked={count}")
		best_so_far = pi
	# try to match input with already filled values
	# list will be empty if none set yet
	# or may contain ints if previous value sets them
	ashift = a >> pi*3
	maskshift = mask >> pi*3
	target = c.p[pi]
	
	for i in range(1024):
		if (ashift & maskshift) != (i & maskshift):
			#print(f"fail {i}: ashift={ashift}, maskshift={maskshift}	")
			continue
		#print(f"  compare: i=0b{i:8b}, ashift=0b{ashift:8b}, maskshift={maskshift:8b}")
		if outputs[i][0] == target:
			#print(f"  found match next: i={i} -> output={outputs[i]}")
			anextshift = ashift | i
			anext = a | (anextshift << (pi*3))
			masknext = mask | (1023 << (pi*3))
			if pi == len(c.p)-1:
				if len(outputs[i]) != 1: # program will have extraneous output
					continue
				if best is None or best > a:
					best = a
					print(f"pi={pi}, solution=0b{a:9b}, decimal={a}, checked={count}")
				continue
					
			#print(f"  q next: anext=0b{anext:8b}, pi={pi+1}")
			q.append((anext, masknext, pi+1))
print(f"checked={count}")
print(f"best a={best}")