import time

class Expr:
    ops = [
        "+",
        "*",
        "/",
        "%",
        "="
    ]
    
    @classmethod
    def from_op(cls, op, a, b):
        return cls(op, [a, b])
        
    @classmethod
    def from_value(cls, a):
        return cls(a)
        
    def __init__(self, value, children=None):
        self.value = value
        self.children = []
        if children is not None:
            for child in children:
                if isinstance(child, Expr):
                    self.children.append(child)
                else:
                    self.children.append(Expr.from_value(child))
                    
    def bracket(self, child):
        if child.has_children():
            return f"({str(child)})"
        else:
            return f"{str(child)}"
    
    def __repr__(self):
        return str(self)
            
    def __str__(self):
        if not self.is_op():
            return str(self.value)
        
        return f"{self.bracket(self.children[0])} {self.value} {self.bracket(self.children[1])}"
    
    def has_children(self):
        return len(self.children) > 0
    
    def is_op(self):
        return self.value in Expr.ops
        
    def is_literal(self):
        return len(self.children) == 0 and type(self.value) == int
    
    def is_variable(self):
        return not self.has_children() and type(self.value) == str
    
    def replace_with(self, other):
        self.value = other.value
        self.children = other.children
        
    def upper_bound(self):
        if self.is_literal():
            return self.value
        elif self.is_variable():
            return 9
        elif self.is_op():
            if self.value == "+":
                return self.children[0].upper_bound() + self.children[1].upper_bound()
            elif self.value == "*":
                return self.children[0].upper_bound() * self.children[1].upper_bound()
            elif self.value == "/":
                return self.children[0].upper_bound() // max(self.children[1].lower_bound(), 1)
            elif self.value == "%":
                return self.children[1].upper_bound() - 1
            elif self.value == "=":
                return 1
    
    def lower_bound(self):
        if self.is_literal():
            return self.value
        elif self.is_variable():
            return 1
        elif self.is_op():
            if self.value == "+":
                return self.children[0].lower_bound() + self.children[1].lower_bound()
            elif self.value == "*":
                return self.children[0].lower_bound() * self.children[1].lower_bound()
            elif self.value == "/":
                return self.children[0].lower_bound() // max(self.children[1].upper_bound(), 1)
            elif self.value == "%":
                return 0
            elif self.value == "=":
                return 0
                
    def all_modulo(self, value):
        if self.value == "*":
            return (self.children[0].is_literal() and self.children[0].value == value 
                    or self.children[1].is_literal() and self.children[1].value == value 
                    or (self.children[0].all_modulo(value) or self.children[1].all_modulo(value)))
        elif self.value == "+":
            return all([c.all_modulo(value) for c in self.children])
        else:
            return False
            
    def is_multiple_of(self, value):
        if self.is_literal():
            return self.value % value == 0
        elif self.value == "*":
            if self.children[0].value == value or self.children[1].value == value:
                return True
        elif self.value == "+":
            return all([c.is_multiple_of(value) for c in self.children()])
        return False
                
    def is_modulo_reducible(self, value):        
        # print(f"checking if {self} is modulo reducible with {value}...")
        if self.value == "+":
            return self.children[0].all_modulo(value) or self.children[1].all_modulo(value)
        elif self.value == "*":
            return self.all_modulo(value)
        return False
            
                
    def distribute_modulo(self, value):
        if self.value == "+":
            for i, child in enumerate(self.children):
                self.children[i] = child.distribute_modulo(value)
            return self
        elif self.value == "*":
            if self.children[0].is_literal() and self.children[0].value == value:
                return Expr.from_value(0)
            elif self.children[1].is_literal() and self.children[1].value == value:
                return Expr.from_value(0)
            else:
                return Expr.from_op("%", self, Expr.from_value(value))
        else:
            return Expr.from_op("%", self, Expr.from_value(value))

    def reduce(self):
        for child in self.children:
            child.reduce()
            
        cidxes = [[0, 1], [1, 0]]
    
        if self.value == "+":
            if self.children[0].value == 0:
                self.replace_with(self.children[1])
            elif self.children[1].value == 0:
                self.replace_with(self.children[0])
            elif self.children[0].is_literal() and self.children[1].is_literal():
                self.value = self.children[0].value + self.children[1].value
                self.children = []
        elif self.value == "*":
            if self.children[0].value == 0 or self.children[1].value == 0:
                self.value = 0
                self.children = []
            elif self.children[0].value == 1:
                self.replace_with(self.children[1])
            elif self.children[1].value == 1:
                self.replace_with(self.children[0])
            elif self.children[0].is_literal() and self.children[1].is_literal():
                self.value = self.children[0].value * self.children[1].value
                self.children = []
        elif self.value == "/":
            if self.children[0].value == 1:
                self.replace_with(self.children[1])
            elif self.children[1].value == 1:
                self.replace_with(self.children[0])
            elif self.children[0].is_literal() and self.children[1].is_literal():
                self.value = self.children[0].value // self.children[1].value
                self.children = []
        elif self.value == "%":
            if self.children[0].is_literal() and self.children[1].is_literal():
                self.value = self.children[0].value % self.children[1].value
                self.children = []
            elif self.children[1].is_literal():
                if self.children[0].value == "+":
                    if self.children[0].children[0].is_multiple_of(self.children[1].value):
                        self.replace_with(self.children[0].children[1])
                    elif self.children[0].children[1].is_multiple_of(self.children[1].value):
                        self.replace_with(self.children[0].children[0])
        elif self.value == "=":
            if self.children[0].is_literal() and self.children[1].is_literal():
                self.value = 1 if self.children[0].value == self.children[1].value else 0
                self.children = []
            elif self.children[0].is_variable():
                if self.children[1].is_literal() and (self.children[1].value < 1 or self.children[1].value > 9):
                    self.value = 0
                    self.children = []
                elif self.children[1].upper_bound() < 1 or self.children[1].lower_bound() > 9:
                    self.value = 0
                    self.children = []
            elif self.children[1].is_variable():
                if self.children[0].is_literal() and (self.children[0].value < 1 or self.children[0].value > 9):
                    self.value = 0
                    self.children = []
                elif self.children[0].upper_bound() < 1 or self.children[0].lower_bound() > 9:
                    self.value = 0
                    self.children = []
            elif str(self.children[0]) == str(self.children[1]):
                self.value = 1
                self.children = []

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
        
    def analyze_line(self, state, program, line_number, inputter):
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
            a = Expr.from_value(int(a))
        if b in state.keys():
            val_b = state[b]        
        elif b is not None:
            val_b = Expr.from_value(int(b))

        if cmd == "inp":
            next_input = next(inputter) # input
            state[a] = Expr.from_value(next_input)
        elif cmd == "add":
            state[a] = Expr.from_op("+", val_a, val_b)
            state[a].reduce()
        elif cmd == "mul":
            state[a] = Expr.from_op("*", val_a, val_b)
            state[a].reduce()
        elif cmd == "div":
            state[a] = Expr.from_op("/", val_a, val_b)
            state[a].reduce()
        elif cmd == "mod":
            state[a] = Expr.from_op("%", val_a, val_b)
            state[a].reduce()
        elif cmd == "eql":
            state[a] = Expr.from_op("=", val_a, val_b)
            state[a].reduce()
        return state
        
    def analyze(self, digits):
        inputter = get_inputter(digits)
        state = {
            "w": Expr.from_value(0),
            "x": Expr.from_value(0),
            "y": Expr.from_value(0),
            "z": Expr.from_value(0)
        }
        for i, line in enumerate(self.program):
            state = self.analyze_line(state, self.program, i, inputter)
            print(f"line={i+1}: state={state}")
            time.sleep(0.01)
        
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

# brute_force_search(program)

program.analyze([f"d{i}" for i in range(14)])

    