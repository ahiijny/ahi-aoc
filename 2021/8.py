LED_SEGMENTS = {
    0: {'a', 'b', 'c,' 'e', 'f', 'g'},      # 6
    1: {'c', 'f'},                          # 2
    2: {'a', 'c', 'd', 'f', 'g'},           # 5
    3: {'a', 'c', 'd', 'f', 'g'},           # 5
    4: {'b', 'c', 'd', 'f'},                # 4
    5: {'a', 'b', 'd', 'f', 'g'},           # 5
    6: {'a', 'b', 'd', 'e', 'f', 'g'},      # 6
    7: {'a', 'c', 'f'},                     # 3
    8: {'a', 'b', 'c', 'd', 'e', 'f', 'g'}, # 7
    9: {'a', 'b', 'c', 'd', 'f', 'g'},      # 6
}

# segment[digit] = led segments corresponding to that digit

def read_hint():
    x = input().split("|")
    hints = x[0].split()
    value = x[1].split()
    
    # normalize segment order
    for i in range(len(hints)):
        hints[i] = ''.join(sorted(hints[i]))
    for i in range(len(value)):
        value[i] = ''.join(sorted(value[i]))
    return hints, value
    
def read_hints():
    all_hints = []
    all_values = []
    while True:
        try:
            hints, value = read_hint()
            all_hints.append(hints)
            all_values.append(value)
        except EOFError:
            break
    return all_hints, all_values

def count_easies(hints, values):
    counts = [0] * 10
    
    for value in values:
        if len(value) == 2:
            counts[1] += 1
        elif len(value) == 3:
            counts[7] +=1
        elif len(value) == 4:
            counts[4] += 1
        elif len(value) == 7:
            counts[8] += 1
    return sum(counts)

hints, values = read_hints()

print(hints)
print(values)

total_count = 0

for hint, value in zip(hints, values):
    total_count += count_easies(hint, value)
    
print(total_count)

