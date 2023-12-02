# https://adventofcode.com/2021/day/1#part2

from collections import deque

prev_total = None
window = deque()
increases = 0

while True:
    try:
        depth = int(input())
        window.append(depth)
        if (len(window) < 3):
            continue
        total = sum(window)
        if prev_total is not None:
            if total > prev_total:
                increases += 1
        prev_total = total
        window.popleft()
    except EOFError:
        break
        
print(increases)
