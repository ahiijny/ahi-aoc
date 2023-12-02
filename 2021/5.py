def read_lines():
    lines = []
    while True:
        try:
            data = input()
            coords_raw = data.split(" -> ")
            coords = []
            for xy in coords_raw:
                coords.append([int(i) for i in xy.split(",")])
            lines.append(coords)
        except EOFError:
            break
    return lines
    
def draw(lines, grid):
    for line in lines:
        a = line[0]
        b = line[1]
        if (a[0] == b[0] or a[1] == b[1]): # only consider vertical or horizontal lines for now
            x1 = min(a[0], b[0])
            x2 = max(a[0], b[0])
            y1 = min(a[1], b[1])
            y2 = max(a[1], b[1])
            for x in range(x1, x2+1):
                for y in range(y1, y2+1):
                    if (x, y) in grid:
                        grid[(x,y)] += 1
                    else:
                        grid[(x,y)] = 1

def count_overlaps(grid):
	return sum(1 for c in grid.values() if c > 1)
    
    
lines = read_lines()
print(lines)
grid = {}
draw(lines, grid)
print(count_overlaps(grid))