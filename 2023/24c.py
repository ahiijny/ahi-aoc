import math
import sympy

ps = []
vs = []

while True:
	try:
		d = input().split('@')
		p = [int(x.strip()) for x in d[0].split(",")]
		v = [int(x.strip()) for x in d[1].split(",")]
		ps.append(p)
		vs.append(v)
	except EOFError:
		break

ts = [sympy.Symbol('r'), sympy.Symbol('s'), sympy.Symbol('t')]

# p
x = sympy.Symbol('x')
y = sympy.Symbol('y')
z = sympy.Symbol('z')

# v
a = sympy.Symbol('a')
b = sympy.Symbol('b')
c = sympy.Symbol('c')

eqns = []


for i, (p,v) in enumerate(zip(ps, vs)):
	eqns.append(x + a * ts[i] - (p[0] + v[0] * ts[i]))
	eqns.append(y + b * ts[i] - (p[1] + v[1] * ts[i]))
	eqns.append(z + c * ts[i] - (p[2] + v[2] * ts[i]))
	if i >= 2:
		break
		
print("paste output into: https://quickmath.com/webMathematica3/quickmath/equations/solve/advanced.jsp")


"""
<<x = 419848807765291,y = 391746659362922,z = 213424530058607,u = -227,v = -221,w = 111,r = 178381243424,s = 564132261724,t = 585444749559>>
"""

print(419848807765291 + 391746659362922 + 213424530058607)



def calc():
	for i in range(len(ps)):
		for j in range(i+1, len(ps)):
			p1 = ps[i]
			p2 = ps[j]
			v1 = vs[i]
			v2 = vs[j]
			
			#print(f"{p1} @ {v1} and {p2} @ {v2}")
			
			# solve system of equations
			M = sympy.Matrix(
				[
					[v1[0], - v2[0], p2[0] - p1[0]],
					[v1[1], - v2[1], p2[1] - p1[1]]
				])
			M_rref, pivots = M.rref()
			
			#print(f"rref={M_rref}, pivots={pivots}")
			
			if 0 not in pivots or 1 not in pivots: # lines do not intersect at one point
				if len(pivots) == 1: # lines are parallel and overlap
					collides[(i,j)] = True
					print(f"{p1} @ {v1} and {p2} @ {v2} are collinear")
				else:
					print(f"{p1} @ {v1} and {p2} @ {v2} are parallel but don't overlap")
				continue
			t1 = M_rref[0,2]
			t2 = M_rref[1,2]
			x = float(p1[0] + t1 * v1[0])
			y = float(p1[1] + t1 * v1[1])
			include = True
			if t1 < 0 or t2 < 0:
				include = False
				#print(f"{p1} @ {v1} and {p2} @ {v2} collide at {(x,y)} in the past")
			elif not (test_area[0] <= x and x <= test_area[1] and test_area[0] <= y and y <= test_area[1]):
				include = False
				#print(f"{p1} @ {v1} and {p2} @ {v2} collide at {(x,y)} outside")
			
			if include:
				collides[(i,j)] = True
				print(f"{p1} @ {v1} and {p2} @ {v2} collide at {(x,y)} inside")

print(f"num collisions: {len(collides)}")
