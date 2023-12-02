A = ['A', 'B', 'C']
X = ['X', 'Y', 'Z']
CHOICE_SCORE = [1, 2, 3] # score[choice] rock, paper, scissors
RESULT_SCORE = {
	-1: 0,
	0: 3,
	1: 6
}

# ROCK_TABLE[a][b] = 1 if A win, 0 if tie, -1 if A loss
ROCK_TABLE = [
	[0, -1, 1],
	[1, 0, -1],
	[-1, 1, 0]
]



def win(opp, you):
	return ROCK_TABLE[you][opp]

total_score = 0

while True:
	try:
		line = input()
		if not line:
			continue
		ax = line.split(' ')
		a = A.index(ax[0])
		x = X.index(ax[1])
		
		result = win(a, x)
		choice_score = CHOICE_SCORE[x]
		result_score = RESULT_SCORE[result]
		score = choice_score + result_score
		total_score += score		
	except EOFError:
		break
		
print(f"total score: {total_score}")
	