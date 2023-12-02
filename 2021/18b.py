import re

class Node:
    INDENT_INTERVAL = 2
    
    @classmethod
    def pair(cls, a, b):
        n = cls()
        n.append(a)
        n.append(b)
        return n
    
    def __init__(self):
        self.parent = None
        self.children = []
        
    def append(self, child):
        self.children.append(child)
        if isinstance(child, Node):
            child.parent = self
            
    def __getitem__(self, i):
        return self.children[i]
        
    def __setitem__(self, i, value):
        self.children[i] = value
        if isinstance(value, Node):
            value.parent = self
        
    def __delitem__(self, i):
        c = self.children[i]
        if isinstance(c, Node):
            c.parent = None
        del self.children[i]
            
    def depth(self):
        d = 0
        n = self
        while n.parent is not None:
            n = n.parent
            d += 1
        return d
        
    def explode(self):
        # print(f"exploding @ {self.get_path()}")
        assert self.parent is not None
        assert len(self.children) == 2
        left = self.children[0]
        right = self.children[1]
        assert(type(left) == int)
        assert(type(right) == int)
        i = self.parent.children.index(self)
        self.add_left(left)
        self.add_right(right)
        self.parent.children[i] = 0
        self.parent = None
        
    def add_left(self, value):
        # print(f"adding left: {value}")
        n = self
        p = self.parent
        going_up = True
        while True:
            if going_up:
                i = p.children.index(n)
                if i == 0: # we are leftmost sibling, need to go further up
                    n = p
                    p = n.parent
                    if p is None: # no more
                        break
                else: # we reached a bridge, can start going down the next sibling
                    going_up = False
                    sibling = p.children[i-1]
                    if isinstance(sibling, Node): # go further down
                        n = sibling
                    else: # found one! just add it here
                        p.children[i-1] += value
                        # print(f"adding left: {value}")
                        break
            else:
                rightmost = n.children[-1]
                if isinstance(rightmost, Node): # go further down
                    p = n
                    n = rightmost
                    if n is None:
                        break
                else:
                    # found one! just add it here
                    n.children[-1] += value
                    # print(f"adding left: {value}")
                    break
                    
    def add_right(self, value):
        # print(f"adding right: {value}")
        n = self
        p = self.parent
        going_up = True
        while True:
            if going_up:
                i = p.children.index(n)
                if i == len(p.children) - 1: # we are rightmost sibling, need to go further up
                    n = p
                    p = n.parent
                    if p is None: # no more
                        break
                else: # we reached a bridge, can start going down the next sibling
                    going_up = False
                    sibling = p.children[i+1]
                    if isinstance(sibling, Node): # go further down
                        n = sibling
                    else: # found one! just add it here
                        p.children[i+1] += value
                        # print(f"adding right: {value}")
                        break
            else:
                leftmost = n.children[0]
                if isinstance(leftmost, Node): # go further down
                    p = n
                    n = leftmost
                    if n is None:
                        break
                else:
                    # found one! just add it here
                    n.children[0] += value
                    # print(f"adding right: {value}")
                    break
        
        
    def split(self, i):
        # print(f"splitting @ {self.get_path()}.{i}")
        assert type(self.children[i]) == int
        assert self.children[i] > 9
        v = self.children[i]
        n = Node()
        a = v // 2
        b = v - a
        n.append(a)
        n.append(b)
        self[i] = n
        
    def reduce(self):
        while True:
            # print(construct_list(self))
            changed = self.reduce_explode()
            if changed:
                continue
            changed = self.reduce_split()
            if changed:
                continue
            if not changed:
                break
                
    def reduce_explode(self):
        if self.depth() >= 4:
            self.explode()
            return True
            
        for i, c in enumerate(self.children):
            if isinstance(c, Node):
                changed = c.reduce_explode()
                if changed:
                    return True
        
        return False
                
        
    def reduce_split(self):
        for i, c in enumerate(self.children):
            if type(c) == int:
                if c >= 10:
                    self.split(i)
                    return True
            elif isinstance(c, Node):
                changed = c.reduce_split()
                if changed:
                    return True
        
        return False
        
    def get_path(self):
        chain = []
        n = self
        while n.parent is not None:
            p = n.parent
            chain.append(str(p.children.index(n)))
            n = p
        chain.reverse()
        return ".".join(chain)
        
    def get_magnitude(self):
        left = self.children[0]
        right = self.children[1]
        if isinstance(left, Node):
            left = left.get_magnitude()
        if isinstance(right, Node):
            right = right.get_magnitude()
        return 3 * left + 2 * right
        
    def __str__(self, depth = 0):
        txt = ""
        for i, c in enumerate(self.children):
            if isinstance(c, Node):
                txt += c.__str__(depth + 1)
            else:
                txt += (f"{depth}\t|" + " " * (depth * Node.INDENT_INTERVAL)) + f"{'-' if i == 0 else ' '} {c}\n"
        return txt
                
        

def read_input():
    nums = []
    while True:
        try:
            line = input()
            assert(re.match("^[0-9[\],]+$", line))
            data = eval(line)
            nums.append(data)
            
        except EOFError:
            break
    return nums
      
def construct_tree(nums):
    node = Node()
    for n in nums:
        if isinstance(n, list):
            c = construct_tree(n)
            node.append(c)
        else:
            node.append(n)
    return node
    
def construct_list(node):
    nums = []
    for c in node:
        if isinstance(c, Node):
            nums.append(construct_list(c))
        else:
            nums.append(c)
    return nums
    
nums = read_input()
print(nums)
print(f"number of snailfish numbers = {len(nums)}")
    
max_mag = None    

# testing all pairs
for i in range(len(nums)):
    for j in range(len(nums)):
        if i == j:
            continue
        print(f"adding snailfish numbers i={i},j={j}...", end=' ')
        a = construct_tree(nums[i])
        b = construct_tree(nums[j])
        n = Node.pair(a, b)
        n.reduce()
        m = n.get_magnitude()
        if max_mag is None or max_mag < m:
            max_mag = m
            print(f"NEW max magnitude: {max_mag}")
        else:
            print(f"    max magnitude: {max_mag}")
