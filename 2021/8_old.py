from pprint import pprint

segments = {
    0: [1, 1, 1, 0, 1, 1, 1], # 6
    1: [0, 0, 1, 0, 0, 1, 0], # 2
    2: [1, 0, 1, 1, 1, 0, 1], # 5
    3: [1, 0, 1, 1, 1, 0, 1], # 5
    4: [0, 1, 1, 1, 0, 1, 1], # 5
    5: [1, 1, 0, 1, 0, 1, 1], # 5
    6: [1, 1, 0, 1, 1, 1, 1], # 6
    7: [1, 0, 1, 0, 0, 1, 0], # 3
    8: [1, 1, 1, 1, 1, 1, 1], # 7
    9: [1, 1, 1, 1, 0, 1, 1], # 6
}

LED_SEGMENTS = {
    0: {'a', 'b', 'c,' 'e', 'f', 'g'},      # 6
    1: {'c', 'f'},                          # 2
    2: {'a', 'c', 'd', 'f', 'g'},           # 5
    3: {'a', 'c', 'd', 'f', 'g'},           # 5
    4: {'b', 'c', 'd', 'f'},                # 5
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
    
def led_to_int(led_set):
    """map from ACTUAL LED ID space to int value"""
    
    for num, segments in LED_SEGMENTS:
        if led_set == segments:
            return num
    
    raise ValueError(led_set)
    
def deduce(hints):
    led_values = { # map from REAL led id space to possible MESSED UP led space ids
        'a': {'a', 'b', 'c', 'd', 'e', 'f', 'g'},
        'b': {'a', 'b', 'c', 'd', 'e', 'f', 'g'},
        'c': {'a', 'b', 'c', 'd', 'e', 'f', 'g'},
        'd': {'a', 'b', 'c', 'd', 'e', 'f', 'g'},
        'e': {'a', 'b', 'c', 'd', 'e', 'f', 'g'},
        'f': {'a', 'b', 'c', 'd', 'e', 'f', 'g'},
        'g': {'a', 'b', 'c', 'd', 'e', 'f', 'g'},
    }
    
    len2 = LED_SEGMENTS[1]
    len3 = LED_SEGMENTS[7]
    
    for hint in hints:
        n = len(hint)
        print(n, end=' ')
        if n == 2:
            for s, v in led_values.items():
                if s in hint:
                    led_values[s] = {s for s in v if s in len2}
                else:
                    led_values[s] = {s for s in v if s not in len2}
        elif n == 3:
            for s, v in led_values.items():
                if s in hint:
                    led_values[s] = {s for s in v if s in len3}
                else:
                    led_values[s] = {s for s in v if s not in len3}
        elif n == 7:
            # provides no new information
            pass
            
     # brute force the rest
     
     index = []
     keys = []
     choices = []
     for s, possible in led_values.items(): # consistent iteration order
        index.append(0)
        keys.append(s)        
        choice.append(list(sorted(possible))
    
    while True:
        # see if assignment of letters is consistent
        actual_to_mess = {}
        for i in range(len(index)):
            actual_to_mess[keys[i]] = choices[i][index[i]]

        # validation check
        for hint in hints:
            for n, leds in LED_SEGMENTS.items():
                
            
        
        
        # increment
        p = 0
        while p < len(index)
            index[p] += 1
            if index[p] >= len(choices[p])
                index[p] = 0
                p +=1
            else:
                break
        if p >= len(index):
            break
            
        
            
    print(led_values)

hints, values = read_hints()

print(hints)
print(values)

for hint in hints:
    deduce(hint)