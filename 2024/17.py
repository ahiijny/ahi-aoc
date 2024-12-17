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
		print(f">adv {x}")
		x = self.op(x)
		self.a = self.a // (2 ** x)
		self.i += 2
		
	def bxl(self, x):
		print(f">bxl {x}")
		self.b = self.b ^ x
		self.i += 2
		
	def bst(self, x):
		print(f">bst {x}")
		x = self.op(x)
		self.b = x % 8
		self.i += 2
		
	def jnz(self, x):
		print(f">jnz {x}")
		if self.a == 0:
			self.i += 2
			return
		self.i = x
		
	def bxc(self, x):
		print(f">bxc {x}")
		self.b = self.b ^ self.c
		self.i += 2
		
	def out(self, x):
		print(f">out {x}")
		x = self.op(x)
		self.stdout.append(x % 8)
		self.i += 2
		
	def bdv(self, x):
		print(f">bdv {x}")
		x = self.op(x)
		self.b = self.a // (2 ** x)
		self.i += 2
		
	def cdv(self, x):
		print(f">cdv {x}")
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
		while self.i < len(self.p):
			print(f"i={self.i}")
			opcode = self.p[self.i]
			operand = self.p[self.i+1]
			f[opcode](operand)
			
		print(",".join([str(x) for x in self.stdout]))
		
c = Code()
c.run()
