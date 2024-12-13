import math

aa = []
bb = []
pp = []

# plus = 0
plus = 10000000000000

try:
	while True:
		a = [x.strip() for x in input().split(":")[1].strip().split(",")]
		b = [x.strip() for x in input().split(":")[1].strip().split(",")]
		c = [x.strip() for x in input().split(":")[1].strip().split(",")]
		
		ax = int(a[0][2:])
		ay = int(a[1][2:])
		aa.append((ax, ay))
		
		bx = int(b[0][2:])
		by = int(b[1][2:])
		bb.append((bx, by))
		
		px = plus + int(c[0][2:])
		py = plus + int(c[1][2:])
		pp.append((px, py))
		input()
except EOFError:
	pass
	
print(aa)
print(bb)
print(pp)

n = 100
costs = []
choices = []

# https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
# https://www.math.cmu.edu/~bkell/21110-2010s/extended-euclidean.html

def extended_gcd(a, b):
	old_r, r = a, b
	old_s, s = 1, 0
	old_t, t = 0, 1
	
	while r != 0:
		q = old_r // r
		
		old_r, r = r, old_r - q * r
		old_s, s = s, old_s - q * s
		old_t, t = t, old_t - q * t
	print(f"gcd({a},{b}: Bézout={old_s},{old_t}, gcd={old_r}, quotients by gcd={t},{s}")
	
	return old_r, old_s, old_t, t, s
	

for i in range(len(aa)):
	print(f"prize={i}")
	min_cost = None
	best_choice = None
	
	xg, xs, xt, xv, xu = extended_gcd(aa[i][0], bb[i][0])
	yg, ys, yt, yv, yu = extended_gcd(aa[i][1], bb[i][1])
	
	# g = gcd(a, b)
	# s a + t b = g
	# u a + v b = 0
	
	if pp[i][0] % xg != 0 or pp[i][1] % yg != 0:
		# no solution
		print(f"no solution for prize {i}")
		continue
	
	xs = xs * pp[i][0] // xg
	xt = xt * pp[i][0] // xg
	ys = ys * pp[i][1] // yg
	yt = yt * pp[i][1] // yg
	
	print(f"initial attempt: {xs} * ax + {xt} * bx = px; {ys} * ay + {yt} * by = py")
	
	# need xs/ys and xt/yt to match, and both to be greater than 0; need to adjust with xu/xv/yu/yv
	
	# find a solution that matches both x and y by controlling j and k
	# found by solving:
	# xu j - yu k = ys - xs
	# xv j - yv k = yt - xt
	# https://en.wikipedia.org/wiki/Cramer%27s_rule
	
	a1 = xu
	b1 = -1 * yu
	c1 = ys - xs
	a2 = xv
	b2 = -1 * yv
	c2 = yt - xt
	
	j = (c1 * b2 - b1 * c2) / (a1 * b2 - b1 * a2)
	k = (a1 * c2 - c1 * a2) / (a1 * b2 - b1 * a2)
	
	print(f"j = {j}, k = {k}")
	
	if j % 1 != 0 or k % 1 != 0:
		print("invalid solution")
		continue
	
	s = xs + j * xu
	t = xt + j * xv
	
	print(f"num a presses = {s}, num b presses = {t}")
	if s < 0 or t < 0:
		print("invalid solution")
		continue
	costs.append(3 * s + t)
	choices.append((s,t))
	
	
print(costs)
print(choices)
	
print(sum([x for x in costs if x is not None]))

