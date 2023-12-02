buckets = []
bucket = []
i = 0
current = 0
best = 0
best_idx = -1

sums = []

while True:
    try:
        amount = input()
        if amount:
            amounti = int(amount)
            bucket.append(amounti)
            current += amounti
        else:
            buckets.append(bucket)
            bucket = []
            if current > best:
                best = current
                best_idx = i
            sums.append((current, i))
            current = 0
            i += 1
    except EOFError:
        break
        
sums.sort(reverse=True)
        
print(f"buckets: {buckets}")
print(f"best: {best}, best_idx: {best_idx}")
print(f"top 3: {sums[:3]}")
print(f"sum top 3: {sum([x[0] for x in sums[:3]])}")
