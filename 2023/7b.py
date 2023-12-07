
def get_order(ch):
	if ch == 'A':
		return 14
	elif ch == 'K':
		return 13
	elif ch == 'Q':
		return 12
	elif ch == 'J':
		return -1
	elif ch == 'T':
		return 10
	return int(ch)
	
def count_sames(h):
	hist = {}
	for c in h:
		if c not in hist:
			hist[c] = 1
		else:
			hist[c] += 1
	return hist
	
TYPE = {
	10: "5",
	9: "4",
	8: "FH",
	7: "3",
	6: "2P",
	5: "1P",
	4: "HC"
}
	
def get_type(h):
	types = []
	for j in range(2, 15):
		h2 = list(h)
		for i in range(len(h2)):
			if h2[i] == -1:
				h2[i] = j
		hist = count_sames(h2)
		if max(hist.values()) == 5:
			types.append(10)
		elif max(hist.values()) == 4:
			types.append(9)
		elif 2 in hist.values() and 3 in hist.values():
			types.append(8)
		elif max(hist.values()) == 3:
			types.append(7)
		elif list(hist.values()).count(2) == 2:
			types.append(6)
		elif list(hist.values()).count(2) == 1:
			types.append(5)
		else:
			types.append(4)
	return max(types)
	
hands = []

while True:
	try:
		line = input().split()
		hand = [get_order(o) for o in line[0].strip()]
		amount = int(line[1])
		
		print(f"hand={hand}, amount={amount}")
		
		t = get_type(hand)
		
		hands.append((t, hand, amount))
		
	except EOFError:
		break
		
hands = sorted(hands, reverse=True)

print(f"hands={list((TYPE[t], hand) for (t, hand, amount) in hands)}")

scores = []
for i in range(len(hands)):
	rank = len(hands) - i
	scores.append(rank * hands[i][2]) 
	print(f"rank={rank}, amount={hands[i][2]}")
		
print(f"winnings={sum(scores)}")