def read_input():
    a = input().split()
    x = a[2]
    x1 = x.split("=")[1].split(",")[0].split("..")
    y = a[3]
    y1 = y.split("=")[1].split("..")
    
    x_range = [int(z) for z in x1]
    y_range = [int(z) for z in y1]
    
    return x_range, y_range
    
def step(s, v):
    s[0] += v[0]
    s[1] += v[1]
    if v[0] > 0:
        v[0] -= 1
    elif v[0] < 0:
        v[0] += 1
    v[1] -= 1
    
def target_is_hit(s, T):
    """return True if the probe went past the target area"""
    # print(f"...{s} in {T}?", end="")
    
    minx = min(T[0][0], T[0][1])
    maxx = max(T[0][0], T[0][1])
    miny = min(T[1][0], T[1][1])
    maxy = max(T[1][0], T[1][1])
    
    if s[0] > maxx or s[1] < miny:
        raise ValueError("flew past")
    elif s[0] >= minx and s[0] <= maxx and s[1] >= miny and s[1] <= maxy:
        return True
    else:
        return False
        
        
def attempt(s, v0, T):
    max_y = s[1]
    s = list(s)
    v = list(v0)
    
    try:
        while True:
            # print(f"{s} ", end='')
            max_y = max(max_y, s[1])
            if target_is_hit(s, T):
                print("hit!", end="")
                return max_y
            step(s, v)
    except ValueError:
        return None
    
def generate_search(T):
    x = 1
    y = 0
    d = 1
    phase = 1
    while True:
        yield x, y
        while y < d:
            y += 1 
            yield x, y
        while x < d + 1:
            x += 1
            yield x, y
        while y > -d:
            y -= 1
            yield x, y
        while x > 1:
            x -= 1
            yield x, y
        d += 1
        while y > -d:
            y -= 1
            yield x, y
        while x < d + 1:
            x += 1
            yield x, y
        while y < d:
            y += 1
            yield x, y
        while x > 1:
            x -= 1
            yield x, y
        d += 1
    
def space_search(T):
    s0 = [0, 0]
    
    overall_max_y = 0
    hit_count = 0
    
    for vx, vy in generate_search(T):
        v0 = [vx, vy]
        print(f"running v0 = {v0}...", end=' ')
        max_y = attempt(s0, v0, T)
        if max_y is None:
            print(f"miss;        \t overall max_y ={overall_max_y}, hit_count={hit_count}")
        else:
            hit_count += 1
            print(f"max_y={max_y}\t overall max_y={overall_max_y}, hit_count={hit_count}")
            if max_y > overall_max_y:
                print(f"new max_y pb: {max_y} with v0 = {v0}")
                overall_max_y = max_y
    
x_range, y_range = read_input()

T = [x_range, y_range]

print(T)

space_search(T)