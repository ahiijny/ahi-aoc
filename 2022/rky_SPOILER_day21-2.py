import re

def try_move1(x, y, d):
    if d == 'u':
        if y == 0 or field[y - 1][x] == ' ':
            new_y = height - 1
            while new_y > y:
                if field[new_y][x] == '.':
                    return (x, new_y)
                elif field[new_y][x] == '#':
                    return (x, y)
                new_y -= 1
            return (x, y)
        else:
            if field[y - 1][x] == '.':
                return (x, y - 1)
            else:
                return (x, y)
    if d == 'd':
        if y == height - 1 or field[y + 1][x] == ' ':
            new_y = 0
            while new_y < y:
                if field[new_y][x] == '.':
                    return (x, new_y)
                elif field[new_y][x] == '#':
                    return (x, y)
                new_y += 1
            return (x, y)
        else:
            if field[y + 1][x] == '.':
                return (x, y + 1)
            else:
                return (x, y)
    if d == 'r':
        if x == width - 1 or field[y][x + 1] == ' ':
            new_x = 0
            while new_x < x:
                if field[y][new_x] == '.':
                    return (new_x, y)
                elif field[y][new_x] == '#':
                    return (x, y)
                new_x += 1
            return (x, y)
        else:
            if field[y][x + 1] == '.':
                return (x + 1, y)
            else:
                return (x, y)
    if d == 'l':
        if x == 0 or field[y][x - 1] == ' ':
            new_x = width - 1
            while new_x > x:
                if field[y][new_x] == '.':
                    return (new_x, y)
                elif field[y][new_x] == '#':
                    return (x, y)
                new_x -= 1
            return (x, y)
        else:
            if field[y][x - 1] == '.':
                return (x - 1, y)
            else:
                return (x, y)

def try_move2(x, y, d):
    if d == 'u':
        if y == 0 and 50 <= x < 100:
            new_x = 0
            new_y = x + 100
            new_d = 'r'
        elif y == 0 and 100 <= x < 150:
            new_x = x - 100
            new_y = 199
            new_d = 'u'
        elif y == 100 and 0 <= x <= 50:
            new_x = 50
            new_y = x + 50
            new_d = 'r'
        else:
            new_x = x
            new_y = y - 1
            new_d = d
    elif d == 'd':
        if y == 199:
            new_x = x + 100
            new_y = 0
            new_d = 'd'
        elif y == 149 and 50 <= x < 100:
            new_x = 49
            new_y = x + 100
            new_d = 'l'
        elif y == 49 and 100 <= x < 150:
            new_x = 99
            new_y = x - 50
            new_d = 'l'
        else:
            new_x = x
            new_y = y + 1
            new_d = 'd'
    elif d == 'r':
        if x == 149:
            new_x = 99
            new_y = 100 + (49 - y)
            new_d = 'l'
        elif x == 99 and 50 <= y < 100:
            new_x = y + 50
            new_y = 49
            new_d = 'u'
        elif x == 99 and 100 <= y < 150:
            new_x = 149
            new_y = 149 - y
            new_d = 'l'
        elif x == 49 and 150 <= y < 200:
            new_x = y - 100
            new_y = 149
            new_d = 'u'
        else:
            new_x = x + 1
            new_y = y
            new_d = 'r'
    else:  # 'l'
        if x == 50 and 0 <= y < 50:
            new_x = 0
            new_y = 100 + (49 - y)
            new_d = 'r'
        elif x == 50 and 50 <= y < 100:
            new_x = y - 50
            new_y = 100
            new_d = 'd'
        elif x == 0 and 100 <= y < 150:
            new_x = 50
            new_y = 149 - y
            new_d = 'r'
        elif x == 0 and 150 <= y < 200:
            new_x = y - 100
            new_y = 0
            new_d = 'd'
        else:
            new_x = x - 1
            new_y = y
            new_d = 'l'
    if field[new_y][new_x] == '.':
        return (new_x, new_y, new_d)
    elif field[new_y][new_x] == ' ':
        print("error")
        return (new_x, new_y, new_d)
    else:
        return (x, y, d)

with open("input.txt", "r") as f:
    lines = [line.rstrip() for line in f]
    cw = {'u': 'r', 'r': 'd', 'd': 'l', 'l': 'u'}
    ccw = {'u': 'l', 'l': 'd', 'd': 'r', 'r': 'u'}
    d_score = {'r': 0, 'd': 1, 'l': 2, 'u': 3}
    height = 0
    while lines[height]:
        height += 1
    width = 1000
    for j in range(height):
        lines[j] = lines[j].ljust(1000)

    field = lines[0: height]
    ins = lines[height + 1]
    n = [int(num) for num in re.findall(r"\d+", ins)]
    r = re.findall(r"[LR]", ins)

    cur_y = 0
    cur_x = field[cur_y].find(".")
    cur_y_2 = 0
    cur_x_2 = cur_x
    dir = 'r'
    dir_2 = 'r'

    for _ in range(n[0]):
        (cur_x, cur_y), (cur_x_2, cur_y_2, dir_2) = try_move1(cur_x, cur_y, dir), try_move2(cur_x_2, cur_y_2, dir_2)
    for j in range(len(r)):
        (dir, dir_2) = (cw[dir], cw[dir_2]) if r[j] == 'R' else (ccw[dir], ccw[dir_2])
        for _ in range(n[j + 1]):
            (cur_x, cur_y), (cur_x_2, cur_y_2, dir_2) = try_move1(cur_x, cur_y, dir), try_move2(cur_x_2, cur_y_2, dir_2)

    print(f"part 1: {4 * (cur_x + 1) + 1000 * (cur_y + 1) + d_score[dir]}")
    print(f"part 2: {4 * (cur_x_2 + 1) + 1000 * (cur_y_2 + 1) + d_score[dir_2]}")
