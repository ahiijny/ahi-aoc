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
        
        x1 = a[0]
        x2 = b[0]
        y1 = a[1]
        y2 = b[1]
        
        dx = None
        dy = None
        
        if (a[0] == b[0]):
            dx = 0
            dy = 1 if y2 > y1 else -1
        elif (a[1] == b[1]):
            dx = 1 if x2 > x1 else -1
            dy = 0
        else:
            dx = 1 if x2 > x1 else -1
            dy = 1 if y2 > y1 else -1
        
        x = x1
        y = y1
        
        while True:
            if (x, y) in grid:
                grid[(x,y)] += 1
            else:
                grid[(x,y)] = 1
                
            x += dx
            y += dy
            
            if (dx > 0 and x > x2 or dx < 0 and x < x2) or (dy > 0 and y > y2 or dy < 0 and y < y2):
                break

def count_overlaps(grid):
	return sum(1 for c in grid.values() if c > 1)
    
    
lines = read_lines()
grid = {}
draw(lines, grid)
print(count_overlaps(grid))