# https://www.reddit.com/r/adventofcode/comments/zqezkn/comment/j0xvrjx/?utm_source=reddit&utm_medium=web2x&context=3

import sys, copy, re
from collections import defaultdict as dd
read = sys.stdin.read
f = open("20.in")

inp = [(x, i) for (i, x) in enumerate(list(map(int,f.read().split('\n'))))]

n = len(inp)

for i in range(n):
    for j in range(n):
        if inp[j][1] == i:
            break
    val = inp[j][0]
    inp.pop(j)
    j = (j + val) % (n - 1)
    inp.insert(j, (val, i))

for z in range(n):
    if inp[z][0] == 0:
        break

nums = [1000, 2000, 3000]
print(sum([inp[(z + nums[i]) % n][0] for i in range(3)]))