def read_input():
    a = int(input().split()[4])
    b = int(input().split()[4])
    return a, b
    
def dice():
    while True:
        for i in range(1, 101):
            yield i
    
def play(a, b):
    rng = dice()
    pos = [a, b]
    scores = [0, 0]
    winner = None
    loser = None
    rolls = 0
    
    while True:
        for i in range(len(pos)):
            a = next(rng)
            b = next(rng)
            c = next(rng)
            rolls += 3
            
            p2 = (pos[i] + a + b + c - 1) % 10 + 1
            scores[i] += p2
            pos[i] = p2
            print(f"Player {i+1} rolls {a}+{b}+{c} and moves to space {pos[i]} for a total score of {scores[i]}")
            if scores[i] >= 1000:
                winner = i
                loser = 0 if winner == 1 else 1
                break
        if winner is not None:
            break
    
    print(f"final: {scores[loser]*rolls}")
    
a, b = read_input()
print(f"{a}, {b}")
play(a, b)

    