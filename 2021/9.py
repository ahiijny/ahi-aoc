def read_grid():
    grid = []
    while True:
        try:
            row = input().strip()
            row = [int(i) for i in row]
            if len(row) > 0:
                grid.append(row)
        except EOFError:
            break
    return grid
    
def calc_risk(grid):
    adj = [
        [1, 0],
        [0, 1],
        [-1, 0],
        [0, -1]
    ]
    H = len(grid)
    W = len(grid[0])
    total_risk = 0
    print(f"H={H}, W={W}")
    for r in range(H):
        for c in range(W):
            h = grid[r][c]
            is_min = True
            for dv in adj:
                r1 = r + dv[0]
                c1 = c + dv[1]
                if 0 <= r1 and r1 < W and 0 <= c1 and c1 < H:
                    other_h = grid[r1][c1]
                    if other_h <= h:
                        is_min = False
                        break
            if is_min:
                print(f"min found at row={r},col={c}")
                total_risk += h + 1
    return total_risk
    
grid = read_grid()
print(calc_risk(grid))
    