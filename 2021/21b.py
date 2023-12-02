def read_input():
    a = int(input().split()[4])
    b = int(input().split()[4])
    return a, b
    
def dice():
    while True:
        for i in range(1, 4):
            yield i
            
def get_3x3():
    scores = [0] * 10
    
    for a in range(1, 4):
        for b in range(1, 4):
            for c in range(1, 4):
                scores[a+b+c] += 1
                
    return scores
    
def play(a, b):
    rng = dice()
    pos = [a, b]
    scores = [0, 0]
    winner = None
    loser = None
    rolls = 0
    
    one_turn = get_3x3()
    print(f"one turn: {one_turn}")
    MAX_SCORE = 32
    MAX_TURNS = 30
    
    # counts[t][p1][s1][p2][s2] = number of universes after t turns with player 1 with score s1 at position p1 and player 2 with score s2 at position p2
    counts = [[[[[0 for s2 in range(MAX_SCORE)] for p2 in range(11)] for s1 in range(MAX_SCORE)] for p1 in range(11)] for t in range(MAX_TURNS)]
    counts[0][a][0][b][0] = 1
    
    for t in range(1, MAX_TURNS):
        player = (t + 1) % 2
        print(f"calculating turn {t} for player {player}:")
        if player == 0:
            for p1 in range(1, 11):
                # print(f"   counting universes where player 1 is at position {p1}:")
                # there are 3^3 different dice rolls scenarios
                for prev_score1 in range(MAX_SCORE):
                     for roll_sum, count in enumerate(one_turn):
                        # there are <count> universes where player rolls roll_sum
                        new_pos = (p1 + roll_sum - 1) % 10 + 1
                        new_score = prev_score1 + new_pos
                        for p2 in range(11):
                            for s2 in range(MAX_SCORE):
                                if prev_score1 >= 21 or s2 >= 21: # game already ended, no more continuation
                                    continue
                                elif new_score >= MAX_SCORE: # the game would have already ended, not worth considering
                                    continue
                                num_universes = counts[t-1][p1][prev_score1][p2][s2] * count
                                counts[t][new_pos][new_score][p2][s2] += num_universes
        elif player == 1:
            for p2 in range(1, 11):
                # print(f"   counting universes where player 2 is at position {p2}:")
                # there are 3^3 different dice rolls scenarios
                for prev_score2 in range(MAX_SCORE):
                     for roll_sum, count in enumerate(one_turn):
                        # there are <count> universes where player rolls roll_sum
                        new_pos = (p2 + roll_sum - 1) % 10 + 1
                        new_score = prev_score2 + new_pos
                        # print(f"> {new_pos}, {new_score}, {count}")
                        for p1 in range(1, 11):
                            for s1 in range(MAX_SCORE):
                                if prev_score2 >= 21 or s1 >= 21: # game already ended, no more continuation
                                    continue
                                elif new_score >= MAX_SCORE: # the game would have already ended, not worth considering
                                    continue
                                num_universes = counts[t-1][p1][s1][p2][prev_score2] * count
                                counts[t][p1][s1][new_pos][new_score] += num_universes
                
        
    player_1_wins = 0
    player_2_wins = 0
    
    for t in range(1, MAX_TURNS):
        for s1 in range(21, MAX_SCORE):
            for s2 in range(0, 21):
                for p1 in range(11):
                    for p2 in range(11):
                        player_1_wins += counts[t][p1][s1][p2][s2]
                        player_2_wins += counts[t][p2][s2][p1][s1]
                        
    print(f"player 1 wins: {player_1_wins} {'*' if player_1_wins > player_2_wins else ''}")
    print(f"player 2 wins: {player_2_wins} {'*' if player_2_wins > player_1_wins else ''}")
    
a, b = read_input()
print(f"{a}, {b}")
play(a, b)

    