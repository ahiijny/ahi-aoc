import math

def get_range(x):
    assign = x.split("=")
    numbers = [int(a) for a in assign[1].split("..")]
    return numbers

def read_input():
    steps = []
    while True:
        try:
            row = input().split()
            on = row[0] == "on"
            ranges = row[1].split(",")
            xranges = get_range(ranges[0])
            yranges = get_range(ranges[1])
            zranges = get_range(ranges[2])
            steps.append({
                "on": on,
                "x": xranges,
                "y": yranges,
                "z": zranges
            })
        except EOFError:
            break
    return steps

def make_3d(X, Y, Z):
    return [[[0 for z in range(Z)] for y in range(Y)] for x in range(X)]
    
def find(cubes, boundaries, x, y, z):
    # print(f"finding ({x},{y},{z}) in cube {cubes} with boundaries {boundaries}")
    xi = 0
    yi = 0
    zi = 0
    while xi < len(boundaries["x"]) and boundaries["x"][xi] <= x: # xi points to the smallest boundary that satisfies boundary > x
        xi += 1
    while yi < len(boundaries["y"]) and boundaries["y"][yi] <= y: # yi points to the smallest boundary that satisfies boundary > y
        yi += 1
    while zi < len(boundaries["z"]) and boundaries["z"][zi] <= z: # zi points to the smallest boundary that satisfies boundary > z
        zi += 1
        
    # print(f"...result: indexes [{xi-1}, {yi-1}, {zi-1}]")
    
    return xi-1, yi-1, zi-1
    
def query(cubes, boundaries, x, y, z):
    xi, yi, zi = find(cubes, boundaries, x, y, z)
    
    return cubes[xi][yi][zi]
    
def split(cubes, boundaries, additions):
    bound_counts = {
        "x": len(boundaries["x"]),
        "y": len(boundaries["y"]),
        "z": len(boundaries["z"]),
    }
    new_boundaries = {
        "x": list(boundaries["x"]),
        "y": list(boundaries["y"]),
        "z": list(boundaries["z"])
    }
    
    for addition in additions:
        axis = addition[0]
        at = addition[1]
        if at in boundaries[axis]: # split already exists at axis, don't need to do anything
            continue
        bound_counts[axis] += 1
        new_boundaries[axis].append(at)
   
    for axis in new_boundaries:
        new_boundaries[axis] = sorted(new_boundaries[axis])
    
    print(f"new_boundaries: {new_boundaries}, bound_counts: {bound_counts}")
    
    new_cubes = make_3d(bound_counts["x"], bound_counts["y"], bound_counts["z"])
                
    return new_cubes, new_boundaries
    
def execute(cubes, boundaries, step):
    on = step["on"]
    xr = step["x"]
    yr = step["y"]
    zr = step["z"]
    
    x1, y1, z1 = find(cubes, boundaries, xr[0], yr[0], zr[0])
    x2, y2, z2 = find(cubes, boundaries, xr[1]+1, yr[1]+1, zr[1]+1)
    
    for xi in range(x1, x2):
        for yi in range(y1, y2):
            for zi in range(z1, z2):
                cubes[xi][yi][zi] = 1 if on else 0
                    
    return cubes, boundaries
                
def count_on(cubes, boundaries):
    count = 0
    
    for xi in range(1, len(cubes)-2):
        dx = boundaries["x"][xi+1] - boundaries["x"][xi]
        print(f"counting xi={xi}...")
        for yi in range(1, len(cubes[xi])-2):
            dy = boundaries["y"][yi+1] - boundaries["y"][yi]
            for zi in range(1, len(cubes[xi][yi])-2):
                dz = boundaries["z"][zi+1] - boundaries["z"][zi]
                count += dx * dy * dz * cubes[xi][yi][zi]
                
    print(f"number of cubes on: {count}")
    
    
steps = read_input()
print(steps)

boundaries = {
    "x": [-math.inf, math.inf],
    "y": [-math.inf, math.inf],
    "z": [-math.inf, math.inf]
}

cubes = make_3d(2, 2, 2)
for xi in range(2):
    for yi in range(2):
        for zi in range(2):
            cubes[xi][yi][zi] = 0
            
splits = []

for step in steps:
    xr = step["x"]
    yr = step["y"]
    zr = step["z"]
    splits.extend([
        ["x", xr[0]],
        ["x", xr[1]+1],
        ["y", yr[0]],
        ["y", yr[1]+1],
        ["z", zr[0]],
        ["z", zr[1]+1]
    ])
    
print(f"all splits: {splits}")
cubes, boundaries = split(cubes, boundaries, splits)
    
for i, step in enumerate(steps):
    print(f"executing step {i}...")
    cubes, boundaries = execute(cubes, boundaries, step)
    
count_on(cubes, boundaries)