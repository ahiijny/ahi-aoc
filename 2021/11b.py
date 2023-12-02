adj = [
    [1, 0],
    [1, 1],
    [0, 1],
    [-1, 1],
    [-1, 0],
    [-1, -1],
    [0, -1],
    [1, -1]
]

def read_grid():
    lines = []
    while True:
        try:
            line = [int(i) for i in input()]
            lines.append(line)
        except EOFError:
            break
    return lines

def copy_grid(grid):
    x = []
    for r in grid:
        rc = []
        for c in r:
            rc.append(c)
        x.append(rc)
    return x
    
def flash(grid, H, W, r, c):
    for dv in adj:
        dr = dv[0]
        dc = dv[1]
        r1 = r + dr
        c1 = c + dc
        if 0 <= r1 and r1 < H and 0 <= c1 and c1 < W:
            grid[r1][c1] += 1
    
def step(grid):
    H = len(grid)
    W = len(grid[0])
    
    flashed = [[False for c in range(W)] for r in range(H)]
    
    for r in range(H):
        for c in range(W):
            grid[r][c] += 1
    
    total_flashes = 0
    while True:
        num_flashes = 0
        for r in range(H):
            for c in range(W):
                if grid[r][c] > 9 and not flashed[r][c]:
                    flash(grid, H, W, r, c)
                    num_flashes += 1
                    flashed[r][c] = True
        if num_flashes == 0:
            break
        else:
            total_flashes += num_flashes
    
    all_flashed = True
    
    for r in range(H):
        for c in range(W):
            if flashed[r][c]:
                grid[r][c] = 0
            else:
                all_flashed = False
    
    return total_flashes, all_flashed

grid = read_grid()
num_flashes = 0
i = 1
while True:
    flashes, all_flashed = step(grid)
    num_flashes += flashes
    if all_flashed:
        print(f"all flashed after step: {i}")
        break
    i += 1
    
print(num_flashes)

