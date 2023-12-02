import operator
from functools import reduce

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
        self.stack = []
        self.depth = 0
        self.indent = ""

    def header(self, i, version, type_id):
        print(f"{self.indent}i={i} header: version={version}, type_id={type_id}")
        self.version_sum += version
        if type_id == 0:
            self.stack.append("sum")
        elif type_id == 1:
            self.stack.append("product")
        elif type_id == 2:
            self.stack.append("minimum")
        elif type_id == 3:
            self.stack.append("maximum")
        elif type_id == 5:
            self.stack.append("greater than")
        elif type_id == 6:
            self.stack.append("less than")
        elif type_id == 7:
            self.stack.append("equal to")
        
    def enter_operator(self, i, length_type, length_value):
        print(f"{self.indent}i={i} >operator: length_type={length_type}, length_value={length_value}")
        self.depth += 1
        self.indent = " " * self.depth * 2
        
    def leave_operator(self, i):
        print(f"{self.indent}i={i} <operator")
        self.depth -= 1
        self.indent = " " * self.depth * 2
        
        # unwind stack
        values = []
        opp = None
        while True:
            x = self.stack.pop()
            if type(x) == str:
                opp = x
                break
            else:
                values.append(x)
        values = list(reversed(values))
        x = None
        if opp == "sum":
            x = sum(values)
        elif opp == "product":
            x = reduce(operator.mul, values, 1)
        elif opp == "minimum":
            x = min(values)
        elif opp == "maximum":
            x = max(values)
        elif opp == "greater than":
            x = 1 if values[0] > values[1] else 0
        elif opp == "less than":
            x = 1 if values[0] < values[1] else 0
        elif opp == "equal to":
            x = 1 if values[0] == values[1] else 0
        else:
            raise ValueError(f"unrecognized operator {opp}")
        
        self.stack.append(x)
            
            
    
    def literal(self, i, n):
        print(f"{self.indent}i={i} literal: n = {n}")
        self.stack.append(n)
    
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
        visitor.enter_operator(i, length_type, length_bits)
        
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
        visitor.enter_operator(i, length_type, packet_count)
        
        i += 1 + 11
        count = 0
        while count < packet_count:
            i, version, type_id = consume_header(bits, i, visitor)
            if type_id == 4:
                i, n = consume_literal(bits, i, visitor)
            else:
                i = consume_operator(bits, i, visitor)
            count += 1
    
    visitor.leave_operator(i)
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
print(v.stack)