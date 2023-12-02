from collections import deque

def get_bits(d, n=4):
    bits = []
    for x in d:
        word = []
        for i in range(n):
            word.append(x & 0x01)
            x >>= 1
        bits.extend(reversed(word))
    return bits

def read_input():
    digits = []
    while True:
        try:
            row = [int(d, 16) for d in input()]
            if len(row) == 0:
                break
            digits.extend(row)
        except EOFError:
            break
    return digits

def btoi(bits):
    x = 0
    for d in bits:
        x *= 2
        x += d
    return x
    
class Visitor:
    def __init__(self):
        self.version_sum = 0
    def header(self, i, version, type_id):
        print(f"i={i} header: version={version}, type_id={type_id}")
        self.version_sum += version
        pass
        
    def operator(self, i, length_type, length_value):
        print(f"i={i} operator: length_type={length_type}, length_value={length_value}")
        pass
    
    def literal(self, i, n):
        print(f"i={i} literal: n = {n}")
        pass
    
def consume_header(bits, i, visitor):
    version = btoi(bits[i:i+3])
    type_id = btoi(bits[i+3:i+6])    
    visitor.header(i, version, type_id)
    
    i += 6
    
    return i, version, type_id
    
def consume_literal(bits, i, visitor):
    b = []
    start = i
    while True:
        b.extend(bits[i+1:i+5])
        i += 5
        
        if bits[i-5] == 0: # last group
            break

    n = btoi(b)
    visitor.literal(start, n)
    
    return i, n
    
def consume_operator(bits, i, visitor):
    length_type = bits[i]
    if length_type == 0:
        length_bits = btoi(bits[i+1:i+1+15])
        visitor.operator(i, length_type, length_bits)
        
        i += 1 + 15
        start = i
        while i - start < length_bits:
            i, version, type_id = consume_header(bits, i, visitor)
            if type_id == 4:
                i, n = consume_literal(bits, i, visitor)
            else:
                i = consume_operator(bits, i, visitor)
                
    else:
        packet_count = btoi(bits[i+1:i+1+11])
        visitor.operator(i, length_type, packet_count)
        
        i += 1 + 11
        count = 0
        while count < packet_count:
            i, version, type_id = consume_header(bits, i, visitor)
            if type_id == 4:
                i, n = consume_literal(bits, i, visitor)
            else:
                i = consume_operator(bits, i, visitor)
            count += 1
            
    return i
    
def parse(bits, visitor):
    i, version, type_id = consume_header(bits, 0, visitor)
    
    if type_id == 4:
        i, n = consume_literal(bits, i, visitor)
    else:
        i = consume_operator(bits, i, visitor)
    
digits = read_input()
print(f"n={len(digits)} {digits}")
bits = get_bits(digits)
print(f"n={len(bits)} {bits}")
v = Visitor()
parse(bits, v)
print(v.version_sum)

    
