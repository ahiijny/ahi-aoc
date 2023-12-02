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

DESIRED_RESULT = [-1, 0, 1]

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
		target_result = DESIRED_RESULT[x]
		
		xc = 0
		for xc in range(3):
			result = win(a, xc)
			if result == target_result:
				break
		choice_score = CHOICE_SCORE[xc]
		result_score = RESULT_SCORE[result]
		score = choice_score + result_score
		total_score += score		
	except EOFError:
		break
		
print(f"total score: {total_score}")
	