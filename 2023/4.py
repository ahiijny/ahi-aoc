total = 0

while True:
	try:
		line = input()
		cards = line.split(":")[1].split("|")
		winning = cards[0].split()
		own = cards[1].split()
		
		worth = 0
		wins = {}
		for win in winning:
			wins[int(win.strip())] = True
		for o in own:
			o = int(o.strip())
			if o in wins:
				if worth == 0:
					worth = 1
				else:
					worth *= 2
		total += worth		
	except EOFError:
		break
		
print(f"total={total}")