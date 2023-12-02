error_score = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

complete_score = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
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
    total_complete_scores = []
    total_error_score = 0
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
            total_error_score += error_score[c]
        else:
            gain = 0
            # no error
            for c in stack[::-1]:
                right = opens[c]
                gain *= 5
                gain += complete_score[right]
            total_complete_scores.append(gain)
    s = sorted(total_complete_scores)
    print(s[len(s)//2])
    
lines = read_code()
score(lines)
