from collections import deque

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
                if 0 <= r1 and r1 < H and 0 <= c1 and c1 < W:
                    other_h = grid[r1][c1]
                    if other_h <= h:
                        is_min = False
                        break
            if is_min:
                print(f"min found at row={r},col={c}")
                total_risk += h + 1
    return total_risk
    
def walk_basins(grid):
    adj = [
        [1, 0],
        [0, 1],
        [-1, 0],
        [0, -1]
    ]
    H = len(grid)
    W = len(grid[0])
    print(f"H={H}, W={W}")
    basin_ids = [[None for i in range(W)] for j in range(H)]
    basin_counter = 0
    for r in range(H):
        for c in range(W):
            if basin_ids[r][c] is not None:
                continue
            if grid[r][c] == 9:
                continue
            walk = deque()
            walk.append((r, c))
            while len(walk) > 0:
                p = walk.popleft()
                if basin_ids[p[0]][p[1]] is not None:
                    continue
                basin_ids[p[0]][p[1]] = basin_counter
                for dv in adj:
                    r1 = p[0] + dv[0]
                    c1 = p[1] + dv[1]
                    if 0 <= r1 and r1 < H and 0 <= c1 and c1 < W:
                        if grid[r1][c1] != 9 and basin_ids[r1][c1] is None:
                            walk.append((r1, c1))
            basin_counter += 1
    total_sizes = {}
    # print_grid(basin_ids)
    for i in range(basin_counter):
        total_sizes[i] = 0
    for r in range(H):
        for c in range(W):
            b = basin_ids[r][c]
            if b is not None:
                total_sizes[b] += 1
    
    return total_sizes
    
def print_grid(g):
    for r in range(len(g)):
        for c in range(len(g[r])):
            print(g[r][c], end='\t')
        print("\n", end='')
    
grid = read_grid()
total_sizes = walk_basins(grid)
print(total_sizes)

largest = sorted(total_sizes.values(), reverse=True)
prod3 = largest[0] * largest[1] * largest[2]

print("product of three largest:", prod3)