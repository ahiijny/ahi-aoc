draw = [int(i) for i in input().split(",")]
boards = []
marks = []

def is_winner(mark):
    for r in range(5):
        row = True
        for c in range(5):
            if not mark[r][c]:
                row = False
                break
        if row: return True
    
    for c in range(5):
        col = True
        for r in range(5):
            if not mark[r][c]:
                col = False
                break
        if col: return True

def mark_board(board, mark, x):
    for r in range(5):
        for c in range(5):
            if board[r][c] == x:
                mark[r][c] = True
                
def score(board, mark, x):
    total = 0
    for r in range(5):
        for c in range(5):
            if not mark[r][c]:
                total += board[r][c]
    return total * x

while True:
    try:
        board = []
        while True:
            row = [int(i) for i in input().split()]
            if len(row) == 0:
                break
            board.append(row)
        if len(board) > 0:
            boards.append(board)
            marks.append([[False for i in range(len(board[0]))] for i in range(len(board))])
    except EOFError:
        break
n = len(boards)
winners = set()
def play():
    for x in draw:
        for i in range(n):
            if i in winners:
                continue
            b = boards[i]
            m = marks[i]
            mark_board(b, m, x)
            if is_winner(m):
                print("board", i, ": ", score(b, m, x))
                winners.add(i)
                

play()
