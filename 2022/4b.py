count = 0

while True:
	try:
		line = input().split(",")
		a = line[0]
		b = line[1]
		
		ra = a.split("-")
		rb = b.split("-")
		
		ra = [int(x) for x in ra]
		rb = [int(x) for x in rb]
		
		print(f"range a: {ra}")
		print(f"range b: {rb}")
		
		a = ra[0]
		b = ra[1]
		x = rb[0]
		y = rb[1]
		
		# a    b
		# | -- |
		#    | -- |
		#    x    y
		
		#       a    b
		#       | -- |
		#    | -- |
		#    x    y
		
		# a          b
		# | -------- |
		#      |-|
		#      x y
		
		#       a b
		#       |-|
		# | ----------- |
		# x             y
		if x <= a and a <= y or x <= b and b <= y or a <= x and x <= b or a <= y and y <= b:
			print("overlap")
			count += 1
		
	except EOFError:
		break
	
print(f"total: {count}")