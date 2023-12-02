def read_grid():
    grid = {}
    folds = []
    maxx = 0
    maxy = 0
    # read grid
    while True:
        pt = input().split(",")
        if len(pt) < 2:
            break
        grid[(int(pt[0]), int(pt[1]))] = "#"
        maxx = max(maxx, int(pt[0]))
        maxy = max(maxy, int(pt[1]))
            
    # read folds
    while True:
        try:
            instr = input().split(" ")
            direc = instr[2].split("=")
            folds.append((direc[0], int(direc[1])))
        except EOFError:
            break
    return grid, folds, maxx, maxy
    
def fold(grid, axis, value, maxx, maxy):
    new_grid = {}
    dim = [maxx, maxy]
    print(f"{axis} fold along {value}:")
    if axis == "x":
        for x in range(2 * value + 1):
            for y in range(maxy + 1):
                if (x, y) in grid:
                    if x <= value:
                        new_grid[(x,y)] = "#"
                        # print(f"keep: ({x},{y})", end=" ")
                    else:
                        new_grid[(value - (x - value), y)] = "#"
                        # print(f"fold: ({x},{y})", end=" ")
    elif axis == "y":
        for x in range(maxx + 1):
            for y in range(2 * value + 1):
                if (x, y) in grid:
                    if y <= value:
                        new_grid[(x,y)] = "#"
                        # print(f"keep: ({x},{y})", end=" ")
                    else:
                        new_grid[(x, value - (y - value))] = "#"
                        # print(f"fold: ({x},{y})", end=" ")
    print()
    return new_grid
    
def print_grid(grid):
    maxx = max((x[0] for x in grid.keys()))
    maxy = max((x[1] for x in grid.keys()))
    for y in range(maxy + 1):
        for x in range(maxx + 1):
            if (x, y) in grid:
                print('#', end='')
            else:
                print('.', end='')
        print()
    
grid, folds, maxx, maxy = read_grid()

# print_grid(grid, maxx, maxy)
print(folds)
print(maxx, maxy)

for f in folds:
    grid = fold(grid, f[0], f[1], maxx, maxy)

print_grid(grid)
