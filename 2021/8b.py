import itertools

LED_SEGMENTS = {
    0: {'a', 'b', 'c,' 'e', 'f', 'g'},      # 6
    1: {'c', 'f'},                          # 2
    2: {'a', 'c', 'd', 'e', 'g'},           # 5
    3: {'a', 'c', 'd', 'f', 'g'},           # 5
    4: {'b', 'c', 'd', 'f'},                # 4
    5: {'a', 'b', 'd', 'f', 'g'},           # 5
    6: {'a', 'b', 'd', 'e', 'f', 'g'},      # 6
    7: {'a', 'c', 'f'},                     # 3
    8: {'a', 'b', 'c', 'd', 'e', 'f', 'g'}, # 7
    9: {'a', 'b', 'c', 'd', 'f', 'g'},      # 6
}

SEGMENTS_TO_NUMBER = {
    'abcefg': 0,    # 6
    'cf': 1,        # 2
    'acdeg': 2,     # 5
    'acdfg': 3,     # 5
    'bcdf': 4,      # 4
    'abdfg': 5,     # 5
    'abdefg': 6,    # 6
    'acf': 7,       # 3
    'abcdefg': 8,   # 7
    'abcdfg': 9     # 6
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
    
def get_original_wires(wires, leds, value):
    # example: wires = [a b c d e f g]
    #          leds =  [d e a f g b c]
    # to get the ORIGINAL segment lit: wires[leds.index(display)]
    
    result = []
    for c in value:
        result.append(wires[leds.index(c)])
    return ''.join(sorted(result))
    
def process(hints, values):
    wires = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    
    num_to_display = None
    display_to_num = None
    
    # brute force yahoo
    for i, leds in enumerate(itertools.permutations(wires)):
        num_to_display = {}
        display_to_num = {}
        for hint in hints: 
            original_wires = get_original_wires(wires, leds, hint)
            if original_wires not in SEGMENTS_TO_NUMBER:
                break # invalid mapping
            num = SEGMENTS_TO_NUMBER[original_wires]
            if num in num_to_display:
                break # duplicate mapping, invalid
            num_to_display[num] = hint
            display_to_num[hint] = num
        if len(display_to_num) == 10:
            print(f"valid mapping found at i={i}: wires={wires}, leds={leds}, mapping={num_to_display}")
            break
   
    x = 0
    for value in values:
        x *= 10
        x += display_to_num[value]
    return x
    
    
hints, values = read_hints()

print(hints)
print(values)

total_sum = 0

for hint, value in zip(hints, values):
    total_sum += process(hint, value)

print(total_sum)
