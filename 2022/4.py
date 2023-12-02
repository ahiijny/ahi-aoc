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
		
		if ra[0] <= rb[0] and rb[1] <= ra[1] or rb[0] <= ra[0] and ra[1] <= rb[1]:
			print("overlap")
			count += 1
		
	except EOFError:
		break
	
print(f"total: {count}")