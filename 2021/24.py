def read_input():
    lines = []
    while True:
        try:
            line = input().split()
            lines.append(line)
        except EOFError:
            break
    return lines

def calc_savepoints(program):
    savepoints = [] # savepoint[i] means there is an input command at line i
    for i, line in enumerate(program):
        if line[0] == "inp":
            savepoints.append(i)
    return savepoints

def get_inputter(digits):
    for digit in digits:
        yield digit
        
def clone_state(state):
    s2 = dict(state)
    s2["consumed"] = list(s2["consumed"])
    return s2

class Program:
    def __init__(self, lines):
        self.program = lines
        self.cache = {}
        savepoints = calc_savepoints(lines)
        print(f"savepoints: {savepoints}")
        
        
    def __str__(self):
        return str(self.program)
        
    def resume(self, digits):
        for i in range(len(digits), 0, -1):
            progress = ''.join([str(d) for d in digits[:i]])
            if progress in self.cache:
                state, line_number = self.cache[progress]
                state = clone_state(state)
                return state, line_number
        return None, None
        
    def execute(self, digits):
        progress = ''.join([str(d) for d in digits])
        inputter = get_inputter(digits)
        state = {
            "w": 0,
            "x": 0,
            "y": 0,
            "z": 0,
            "consumed": []
        }
        start_i = 0
        resume_state, resume_i = self.resume(digits)
        if resume_state is not None:
            state = resume_state
            start_i = resume_i
            for i in range(len(state["consumed"])): # skipped inputs
                next(inputter)
        
        # print(f"running from i={start_i},state={state} for input={progress}")
        for i in range(start_i, len(self.program)):
            state = self.process(state, self.program, i, inputter)
        valid = state["z"] == 0
        if valid:
            print(f"valid model number: {''.join([str(d) for d in digits])}")
        
    def process(self, state, program, line_number, inputter):
        stmt = program[line_number]
        cmd = stmt[0]
        a = stmt[1]
        b = None
        if len(stmt) > 2:
            b = stmt[2]
        val_a = a
        val_b = b
        if a in state.keys():
            val_a = state[a]
        else:
            a = int(a)
        if b in state.keys():
            val_b = state[b]        
        elif b is not None:
            val_b = int(b)

        if cmd == "inp":
            # store cache
            progress = ''.join([str(d) for d in state["consumed"]])
            if progress not in self.cache:
                self.cache[progress] = (clone_state(state), line_number)
                if len(state["consumed"]) < 6:
                    print(f"adding to cache: {progress} = {self.cache[progress]}")
            # else:
            #     print(f"consumed state {progress} already in cache")
        
            state[a] = next(inputter) # input
            state["consumed"].append(state[a])
            # if state[a] != 9:
                # print(f"ZOMG not a 9!!!! {state[a]}")
            
        elif cmd == "add":
            state[a] = val_a + val_b
        elif cmd == "mul":
            state[a] = val_a * val_b
        elif cmd == "div":
            state[a] = val_a // val_b
        elif cmd == "mod":
            state[a] = val_a % val_b
        elif cmd == "eql":
            state[a] = 1 if val_a == val_b else 0
        return state
        
def decrement(digits):
    for i in range(len(digits)-1, -1, -1):
        digits[i] -= 1
        if digits[i] >= 0:
            break
        else:
            digits[i] = 9
            
def is_done(digits):
    for d in digits:
        if d != 0:
            return False
    return True
    
def brute_force_search(program):
    # search digits
    digits = [9 for i in range(14)]
    log_next = None
    LOG_INTERVAL = 10000

    while not is_done(digits):
        current = int(''.join([str(d) for d in digits]))
        if log_next is None or current < log_next:
            print(f"testing: {current}")
            log_next = current - LOG_INTERVAL
        valid = program.execute(digits)
        if valid:
            break
        else:
            while True:
                decrement(digits)
                if 0 not in digits:
                    break
            
program = Program(read_input())
print(program)   

brute_force_search(program)
    