# https://adventofcode.com/2021/day/1

prev = None
increases = 0

while True:
    try:
        depth = int(input())
        if prev is not None:
            if depth > prev:
                increases += 1
        prev = depth
    except EOFError:
        break
        
print(increases)
