def read_input():
    grid = []
    while True:
        try:
            line = input()
            grid.append([c for c in line])
        except EOFError:
            break
    return grid

def clone(grid):
    new_grid = []
    for row in grid:
        new_grid.append(list(row))
    return new_grid
    
def right(c, grid):
    W = len(grid[0])
    
    c += 1
    if c == W:
        c = 0
    return c
    
def left(c, grid):
    W = len(grid[0])
    
    c -= 1
    if c == -1:
        c = W-1
    return c
    
def up(r, grid):
    H = len(grid)
    
    r -= 1
    if r == -1:
        r = H-1
    return r

def down(r, grid):
    H = len(grid)
    
    r += 1
    if r == H:
        r = 0
    return r
    
def step(grid):
    H = len(grid)
    W = len(grid[0])
        
    new_grid = clone(grid)
    
    # horizontallers first
    
    moved = 0
    
    for r in range(H):
        for c in range(W):
            cell = grid[r][c]
            if cell == ">":
                new_c = right(c, grid)
                if grid[r][new_c] == ".":
                    new_grid[r][new_c] = ">"
                    moved += 1
                    new_grid[r][c] = "."
                    
    # then verticallers
    
    newer_grid = clone(new_grid)
    
    for r in range(H):
        for c in range(W):
            cell = new_grid[r][c]
            if cell == "v":
                new_r = down(r, grid)
                if new_grid[new_r][c] == ".":
                    newer_grid[new_r][c] = "v"
                    moved += 1
                    newer_grid[r][c] = "."
                    
    return newer_grid, moved
    
    
grid = read_input()
print(grid)

i = 0
moved = 0

while True:
    grid, moved = step(grid)
    i += 1
    print(f"step {i}: moved = {moved}")
    if moved == 0:
        break
