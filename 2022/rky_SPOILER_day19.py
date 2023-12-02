import re


def div_up(x, y):
    return (x + y - 1) // y


def find_quality(b, n, or_lim, cl_lim, ob_lim):
    max_geodes = 0

    def dfs(c):
        nonlocal max_geodes, n, or_lim, cl_lim, ob_lim
        if c[7] + (n - c[8]) * c[6] + ((n - c[8]) * (n - c[8] - 1)) / 2 <= max_geodes:
            return

        if c[8] <= n:
            if c[7] + c[6] * (n - c[8]) > max_geodes:
                max_geodes = c[7] + c[6] * (n - c[8])
        else:
            return

        if c[0] < or_lim:
            or_c = max(0, div_up(b[1] - c[1], c[0])) + 1
            dfs((c[0] + 1, c[1] + c[0] * or_c - b[1], c[2], c[3] + c[2] * or_c, c[4], c[5] + c[4] * or_c, c[6], c[7] + c[6] * or_c, c[8] + or_c))

        if c[2] < cl_lim:
            cl_c = max(0, div_up(b[2] - c[1], c[0])) + 1
            dfs((c[0], c[1] + c[0] * cl_c - b[2], c[2] + 1, c[3] + c[2] * cl_c, c[4], c[5] + c[4] * cl_c, c[6], c[7] + c[6] * cl_c, c[8] + cl_c))

        if c[4] < ob_lim and c[2]:
            ob_c = max(0, div_up(b[3] - c[1], c[0]), div_up(b[4] - c[3], c[2])) + 1
            dfs((c[0], c[1] + c[0] * ob_c - b[3], c[2], c[3] + c[2] * ob_c - b[4], c[4] + 1, c[5] + c[4] * ob_c, c[6], c[7] + c[6] * ob_c, c[8] + ob_c))

        if c[4]:
            ge_c = max(0, div_up(b[5] - c[1], c[0]), div_up(b[6] - c[5], c[4])) + 1
            dfs((c[0], c[1] + c[0] * ge_c - b[5], c[2], c[3] + c[2] * ge_c, c[4], c[5] + c[4] * ge_c - b[6], c[6] + 1, c[7] + c[6] * ge_c, c[8] + ge_c))

    dfs((1, 2, 0, 0, 0, 0, 0, 0, 2))
    print(f"blueprint: {b[0]} max: {max_geodes}")
    return max_geodes


with open("input.txt", "r") as f:
    lines = [line.rstrip() for line in f]
    blueprints = []

    for line in lines:
        blueprints.append([int(n) for n in re.findall(r"\d+", line)])

    s = 0
    for b in blueprints:
        s += find_quality(b, 24, 4, 10, 10) * b[0]
    print(f"part 1: {s}")

    m = 1
    for b in blueprints[:3]:
        m *= find_quality(b, 32, 4, 10, 10)
    print(f"part 2: {m}")
