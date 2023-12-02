from collections import deque

gt_0 = []
m_total = 0
distances = {}


def rec(open, total, time, c_dest, e_dest, c_eta, e_eta):
    global m_total
    open = open.copy()
    time += 1
    total += sum(d[k][0] for k in open)
    if time == 26:
        if total > m_total:
            print(total)
            m_total = total
        return total

    c_eta -= 1
    e_eta -= 1
    if c_eta == 0:
        open.add(c_dest)
    if e_eta == 0:
        open.add(e_dest)

    to_reach = {n[0]: n[1] for n in gt_0 if n[0] not in open and n[0] and n[0] != c_dest and n[0] != e_dest}

    c_paths = []
    if c_eta == -1:
        c_paths = [r for r in distances[c_dest] if r[1] + time < 26 and r[0] in to_reach]

    e_paths = []
    if e_eta == -1:
        e_paths = [r for r in distances[e_dest] if r[1] + time < 26 and r[0] in to_reach]

    if e_eta == -1 and len(e_paths) != 0 and c_eta == -1 and len(c_paths) != 0:
        m_ret = 0
        for a in c_paths:
            for b in e_paths:
                m_ret = max(rec(open, total, time, a[0], b[0], a[1], b[1]), m_ret)
        return m_ret
    elif e_eta == -1 and len(e_paths) != 0:
        return max(rec(open, total, time, c_dest, b[0], c_eta, b[1]) for b in e_paths)
    elif c_eta == -1 and len(c_paths) != 0:
        return max(rec(open, total, time, a[0], e_dest, a[1], e_eta) for a in c_paths)
    else:
        return rec(open, total, time, c_dest, e_dest, c_eta, e_eta)


with open("input.txt", "r") as f:
    lines = [line.rstrip() for line in f]
    d = {}
    for line in lines:
        line = line.split()
        flow = int(line[4].split('=')[1][0:-1])
        d[line[1]] = (flow, [l.rstrip(',') for l in line[9:]])
    for start in d:
        q = deque()
        q.append((start, 0))
        visited = {start}
        dist = []
        while q:
            c = q.popleft()
            dist.append(c)
            for n in d[c[0]][1]:
                if n not in visited:
                    q.append((n, c[1] + 1))
                    visited.add(n)
        distances[start] = dist

    for key in d:
        if d[key][0] > 0:
            gt_0.append((key, d[key][0]))
    print(rec(set(), 0, 0, 'AA', 'AA', 0, 0))
