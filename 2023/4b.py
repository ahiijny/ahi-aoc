total = 0

counts = {}
i = 1

while True:
	try:
		line = input()
		if i not in counts:
			counts[i] = 1
		else:
			counts[i] += 1
		cards = line.split(":")[1].split("|")
		winning = cards[0].split()
		own = cards[1].split()
		
		wincount = 0
		wins = {}
		for win in winning:
			wins[int(win.strip())] = True
		for o in own:
			o = int(o.strip())
			if o in wins:
				wincount += 1
		print(f"card {i}: winning cards = {wincount}")
		for j in range(1, wincount+1):
			new_card = i + j
			gain = counts[i]
			if new_card in counts:
				counts[new_card] += gain
			else:
				counts[new_card] = gain
		i += 1
	except EOFError:
		break

print(f"counts={counts}")
print(f"total cards={sum(counts.values())}")