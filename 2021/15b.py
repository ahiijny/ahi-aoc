from collections import deque

def read_input():
    grid = []
    while True:
        try:
            row = [int(r) for r in input()]
            grid.append(row)
        except EOFError:
            break
    return grid
    
def extend_grid(grid):
    H = len(grid)
    W = len(grid[0])
    
    new_grid = [[None for c in range(5 * W)] for r in range(5 * H)]
    
    for ir in range(5):
        for ic in range(5):
            for r in range(H):
                for c in range(W):
                    value = ((grid[r][c] + ir + ic - 1) % 9) + 1
                    new_grid[ir*H + r][ic*W + c] = value
                
    return new_grid
    
    
def walk(grid):
    """dp solution"""
    W = len(grid)
    H = len(grid[0])
    print(f"H={H}, W={W}")
    
    # row column
    adj = [
        [1, 0],
        [0, 1],
        [-1, 0],
        [0, -1]
    ]
    
    q = deque()
    q.append((0, [0, 0], [])) # risk, location, path
    min_risk = [[[None for c in range(len(grid[0]))] for r in range(len(grid))] for u in range(W + H + 100)]
    
    print(len(min_risk[0][0]))
    
    # min_risk[path_length][row][column]
    
    min_risk[0][0][0] = 0
            
    d = 1
    while d < W + H + 100:        
        print(f"filling d={d}", end=" ")
        
        for r in range(H):
            for c in range(W):
                if r + c > d: # won't be reachable here anyway
                    continue
                risks = []
                if min_risk[d-1][r][c] is not None:
                    risks.append(min_risk[d-1][r][c])
                for dv in adj:
                    prev = [r + dv[0], c + dv[1]]
                    if prev[0] < 0 or prev[0] >= H or prev[1] < 0 or prev[1] >= W:
                        continue
                    if min_risk[d-1][prev[0]][prev[1]] is None:
                        continue
                    risks.append(min_risk[d-1][prev[0]][prev[1]] + grid[r][c])
                if len(risks) > 0:
                    min_risk[d][r][c] = min(risks)
        if min_risk[d][H-1][W-1] is not None:
            print(f"min risk to reach position ({H-1},{W-1}): {min_risk[d][H-1][W-1]}")
        else:
            print()
        d += 1
    
grid = read_input()
H = len(grid)
W = len(grid[0])

grid = extend_grid(grid)
print(len(grid), len(grid[0]))

for ir in range(5):
    for ic in range(5):
        print(grid[ir * H][ic * W], end=' ')
    print()

walk(grid)
