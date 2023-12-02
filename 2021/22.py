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
    
def execute(cubes, step):
    on = step["on"]
    xr = step["x"]
    yr = step["y"]
    zr = step["z"]
    
    for x in range(xr[0], xr[1]+1):
        for y in range(yr[0], yr[1]+1):
            for z in range(zr[0], zr[1]+1):
                cubes[(x,y,z)] = on
                
def count_on(cubes):
    count = sum([1 if on else 0 for on in cubes.values()])
    print(f"number of cubes on: {count}")
    
    
steps = read_input()
print(steps)

cubes = {}

for x in range(-50, 51):
    for y in range(-50, 51):
        for z in range(-50, 51):
            cubes[(x, y, z)] = False
            
for i, step in enumerate(steps):
    print(f"executing step {i}...")
    execute(cubes, step)
    
count_on(cubes)

    