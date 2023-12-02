import random
import re

points = []


def dist(x, y):
    coords = [val[2] - abs(x - val[0]) - abs(val[1] - y) + 1 for val in points if abs(x - val[0]) + abs(val[1] - y) <= val[2]]
    if len(coords) == 0:
        return 0
    return max(coords)


with open("15.in", "r") as f:
    lines = [line.rstrip() for line in f]
    for line in lines:
        s = re.split(r'[=,:]', line)
        x, y, b_x, b_y = int(s[1]), int(s[3]), int(s[5]), int(s[7])
        m_dist = abs(x - b_x) + abs(y - b_y)
        points.append((x, y, m_dist))
    min_d = 1234567890
    flag = True
    while flag:
        x = random.randint(0, 4000000)
        y = random.randint(0, 4000000)
        d = dist(x, y)
        if dist(x, y) < 100000:
            while True:
                if d == 0:
                    flag = False
                if x > 0 and dist(x - 1, y) < d:
                    d = dist(x - 1, y)
                    x -= 1
                elif x < 4000000 and dist(x + 1, y) < d:
                    d = dist(x + 1, y)
                    x += 1
                elif y > 0 and dist(x, y - 1) < d:
                    d = dist(x, y - 1)
                    y -= 1
                elif y < 4000000 and dist(x, y + 1) < d:
                    d = dist(x, y + 1)
                    y += 1
                else:
                    min_d = min(min_d, d)
                    print(f"dist: {d}, min dist: {min_d}, x: {x}, y: {y}")
                    if min_d == 0:
                        flag = False
                    break
