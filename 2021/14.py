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
    
def step(template, rules):
    next_seq = []
    
    for i in range(len(template) - 1):
        a = template[i]
        b = template[i+1]
        next_seq.append(a)
        for r in rules:
            if a == r[0][0] and b == r[0][1]:
                next_seq.append(r[1])
    next_seq.append(template[-1])
    return next_seq
    
template, rules = read_input()

print(template)
print(rules)

for i in range(10):
    template = step(template, rules)
    
hist = {}

for c in template:
    if c in hist:
        hist[c] += 1
    else:
        hist[c] = 1

print(hist)
        
max_e = max([v for v in hist.values()])
min_e = min([v for v in hist.values()])

print(max_e - min_e)

