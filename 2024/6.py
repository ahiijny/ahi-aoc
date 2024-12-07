grid = []
visited = {}

dirs = [
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0)
    ]
di = 0
start = None

with open('6.in') as f:
    for y, line in enumerate(f):
        grid.append(line.strip())
        for x, p in enumerate(grid[y]):
            if p == '^':
                start = (x, y)
def bounded(x, y):
    return 0 <= x and x < len(grid[0]) and 0 <= y and y < len(grid)
print(grid)

p = start
while bounded(*p):
    d = dirs[di]
    visited[p] = True
    p2 = (p[0] + d[0], p[1]+d[1])
    if not bounded(*p2):
        break
    if grid[p2[1]][p2[0]] == '#':
        di = (di + 1) % 4
        continue
    p = p2
    
print(len(visited))
