error_score = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

opens = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}

closes = {
    ')': '(',
    ']': '[',
    '}': '{',
    '>': '<',
}

def read_code():
    lines = []
    while True:
        try:
            line = input()
            lines.append(line)
        except EOFError:
            break
    return lines
    
def score(lines):
    total_score = 0
    for line in lines:
        stack = []
        try:
            for c in line:
                if c in opens:
                    stack.append(c)
                elif c in closes:
                    left = closes[c]
                    if len(stack) == 0 or stack[-1] != left:
                        raise ValueError()
                    stack.pop()
        except ValueError:
            total_score += error_score[c]
    print(total_score)
    
lines = read_code()
score(lines)
