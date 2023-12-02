def read_input():
    template = input()
    input()
    rules = []
    
    while True:
        try:
            r = input().split(" -> ")
            if len(r) == 0:
                break
            rules.append(r)
        except EOFError:
            break
    return template, rules

def convert(template):
    first = template[0]
    last = template[-1]
    pairs = {}
    for i in range(len(template) - 1):
        pair = template[i] + template[i+1]
        # print(pair, end=" ")
        if pair not in pairs:
            pairs[pair] = 1
        else:
            pairs[pair] += 1
    return pairs, first, last
    
def step(pairs, first, last, rules):
    next_pairs = {}
    
    for pair, count in pairs.items():
        for r in rules:
            if pair == r[0]:
                new_pairs = [pair[0] + r[1], r[1] + pair[1]]
                for new_pair in new_pairs:
                    if new_pair not in next_pairs:
                        next_pairs[new_pair] = count
                    else:
                        next_pairs[new_pair] += count
    return next_pairs, first, last
    
template, rules = read_input()

print(template)
print(rules)

pairs, first, last = convert(template)
print(pairs)

for i in range(40):
    print(i)
    pairs, first, last = step(pairs, first, last, rules)

print(pairs, first, last)    

# count individual letters

counts = {}
for pair, count in pairs.items():
    letters = [pair[0], pair[1]]
    for a in letters:
        if a in counts:
            counts[a] += count
        else:
            counts[a] = count

# only the first and last letter are not counted twice

counts[first] += 1
counts[last] += 1

# remove double counts

counts = {k: v/2 for (k, v) in counts.items()}
print(counts)

max_e = max([v for v in counts.values()])
min_e = min([v for v in counts.values()])

print(max_e - min_e)

