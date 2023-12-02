from statistics import mode
from collections import deque

def read_input():
    scanners = []

    beacons = None
    try:
        while True:
            line = input()
            if "---" in line:
                if beacons is not None:
                    scanners.append(beacons)
                beacons = []
            elif line.strip() == "":
                continue
            else:
                beacons.append([int(i) for i in line.split(",")])
    except EOFError:
        pass
    if beacons is not None:
        scanners.append(beacons)
    return scanners

def plus(a, b):
    return [a[i] + b[i] for i in range(len(a))]

def minus(a, b):
    return [a[i] - b[i] for i in range(len(a))]
    
def times(a, b):
    return [a[i] * b[i] for i in range(len(a))]
    
def eqabs(a, b):
    for ai, bi in zip(a, b):
        if abs(ai) != abs(bi):
            return False
    return True
    
def sign(a):
    if a > 0:
        return 1
    elif a < 0:
        return -1
    else:
        return 0
    
def signdiff(a, b):
    """sign difference from a to b"""
    return [sign(a[i]) * sign(b[i]) for i in range(len(a))]
    
def mul(A, u):
    # multiply a matrix and a vector
    assert(len(A[0]) == len(u))
    v = []
    for r in range(len(A)):
        cell = 0
        for c in range(len(A[r])):
            cell += A[r][c] * u[c]
        v.append(cell)
    return v

def mulmat(A, B):
    assert(len(A[0]) == len(B))
    C = [[None for c in range(len(B[0]))] for r in range(len(A))]
    for r in range(len(A)):
        for c in range(len(B[0])):
            C[r][c] = sum([A[r][k] * B[k][c] for k in range(len(B))])
    return C

class Transform:
    def __init__(self):
        self.A = None
        
    @classmethod
    def identity(cls):
        return cls.from_transform()

    @classmethod
    def from_transform(cls, dx=0, dy=0, dz=0, e1=[1, 0, 0], e2=[0, 1, 0], e3=[0, 0, 1]):
        """https://en.wikipedia.org/wiki/Transformation_matrix
        
        Represents a transfromation from space 1 to space 2, where:
        
        [dx, dy, dz] = the origin of S2 in S1 coordinates
        e1 = the unit basis vector for S2's x axis, in S1's coordinates
        e2 = the unit basis vector for S2's y axis, in S1's coordinates
        e3 = the unit basis vector for S2's z axis, in S1's coordinates
        
        e.g. suppose S2 is just S1 but with y and z axes rotated 90 degrees so that z now points up and y points away
        
        then the affine matrix for that would be:
        
        [1  0  0  0]
        [0  0  1  0]
        [0  -1 0  0]
        [0  0  0  1]
        
        assuming all vectors are augmented with a 1 at the end
        
        
        """
        self = cls()
        self.A = [[0 for c in range(4)] for r in range(4)]
        
        self.A[0][3] = dx
        self.A[1][3] = dy
        self.A[2][3] = dz
        self.A[3][3] = 1
        
        self.A[0][0] = e1[0]
        self.A[1][0] = e1[1]
        self.A[2][0] = e1[2]
        
        self.A[0][1] = e2[0]
        self.A[1][1] = e2[1]
        self.A[2][1] = e2[2]
        
        self.A[0][2] = e3[0]
        self.A[1][2] = e3[1]
        self.A[2][2] = e3[2]
        return self
        
    @classmethod
    def compound(cls, A, B):
        """transform B, then A)"""
        C = mulmat(A.A, B.A)
        self = cls()
        self.A = C
        return self
        
    def transform(self, point):
        assert len(point) == 3
        # augment
        p = list(point)
        p.append(1)
        
        result = mul(self.A, p)
        return result[0:3]
        
    @staticmethod
    def get_rotations():
        e1 = [1, 0, 0]
        e1m = [-1, 0, 0]
        e2 = [0, 1, 0]
        e2m = [0, -1, 0]
        e3 = [0, 0, 1]
        e3m = [0, 0, -1]
        
        bases = [
            [e1, e2, e3],
            [e1, e3, e2m],
            [e1, e2m, e3m],
            [e1, e3m, e2],
            [e1m, e2, e3m],
            [e1m, e3, e2],
            [e1m, e2m, e3],
            [e1m, e3m, e2m],
            [e2, e1, e3m],
            [e2, e3m, e1m],
            [e2, e1m, e3],
            [e2, e3, e1],
            [e2m, e1, e3],
            [e2m, e3m, e1],
            [e2m, e1m, e3m],
            [e2m, e3, e1m],
            [e3, e1, e2],
            [e3, e2, e1m],
            [e3, e1m, e2m],
            [e3, e2m, e1],
            [e3m, e1, e2m],
            [e3m, e2, e1],
            [e3m, e1m, e2],
            [e3m, e2m, e1m]
        ]
        
        transforms = []
        for base in bases:
            transforms.append(Transform.from_transform(e1=base[0], e2=base[1], e3=base[2]))
            
        inverses = {} # index the inverse transformations
        for i, t1 in enumerate(transforms):
            for j, t2 in enumerate(transforms):
                u1 = [1, 0, 0]
                u2 = [0, 1, 0]
                u3 = [0, 0, 1]
                v1 = t2.transform(t1.transform(u1))
                v2 = t2.transform(t1.transform(u2))
                v3 = t2.transform(t1.transform(u3))
                if [u1, u2, u3] == [v1, v2, v3]:
                    print(f"rot {j} is an inverse of rot {i}")
                    inverses[i] = j
                    
        print(f"rotations with inverses: {sorted(inverses.keys())}")
                    
        return transforms, inverses
        
    def __repr__(self):
        return str(self.A)
        
    def __str__(self, indent=0):
        res = "["
        for i, r in enumerate(self.A):
            res += ("" if i == 0 else " " * indent) + str(r) + ("" if i == len(self.A) - 1 else ",\n")
        res += "]"
        return res

class Space:
    def __init__(self, points=[]):
        self.points = []
        self.points.extend(points) # relative to self space
        self.relations = {}
        
    def calc_pair_fingerprints(self):
        """calculate vectors between all pairs of points. using the specific integer values as a fingerprint of sorts"""
        pairs = {}
        sigs = {}
        for i in range(len(self.points)):
            for j in range(i+1, len(self.points)):                
                points = sorted([self.points[i], self.points[j]]) # stable order
                idx_1 = i if points[0] == self.points[i] else j
                idx_2 = j if points[1] == self.points[j] else i
                diff = minus(points[1], points[0])
                print(f"{idx_1}-{idx_2}: {diff}")
                pairs[(idx_1, idx_2)] = diff
                
                sig = tuple(sorted([abs(c) for c in diff]))
                if sig not in sigs:
                    sigs[sig] = [(idx_1, idx_2)]
                else:
                    sigs[sig].append((idx_1, idx_2))
                
        return pairs, sigs
    
def find_matches(pairs, sigs):
    """
    pairs[i] = dict of pairs for space i, where dict[(i, j)] gives the pt[i]->pt[j] vector
    sigs[i] = dict of vector diff fingerprints for space i, where dict[(x, y, z)] gives the list of point pairs [(i1, j1), (i2, j2)] that yield the sig (x, y, z)
    
    return: matches[(i,j)] = [a, b, c, d] is a signature match between spaces i and j, between points a->b in space i and points c->d in space j
    """
    
    matches = {}
    for i in range(len(sigs)):  
        for j in range(i+1, len(sigs)):
            print(f"comparing signatures for spaces {i} and {j}:")
            sig1 = sigs[i]
            sig2 = sigs[j]
            
            overlap = sig1.keys() & sig2.keys()
            if len(overlap) == 0:
                continue
                
            for sig in overlap:
                pairs1 = sig1[sig]
                pairs2 = sig2[sig]
                
                if len(pairs1) > 1:
                    print(f" more than one signature match in space {i} for vector diff signature {sig}; skipping")
                    continue
                elif len(pairs2) > 1:
                    print(f" more than one signature match in space {j} for vector diff signature {sig}; skipping")
                    continue
                    
                a = pairs1[0][0]
                b = pairs1[0][1]
                c = pairs2[0][0]
                d = pairs2[0][1]                
        
                print(f"  found a match in {i}:[{a}][{b}] and {j}:[{c}][{d}]: {pairs[i][(a,b)]} and {pairs[j][(c,d)]}")
                if (i,j) not in matches:
                    matches[(i,j)] = [[a, b, c, d]]
                else:
                    matches[(i,j)].append([a, b, c, d])
    return matches
    
def compute_rotations(spaces, pairs, sigs, matches):
    """
        spaces[i] = space i
        pairs[i] = dict of all point pairs in space i, where dict[(i,j)] is the vector from point i to point j
        sigs[i] = dict of all vector fingerprints in space i, where dict[(x,y,z)] = the list of points (a,b) where the vector a->b have that signature
        matches[i] = dict of all fingerprint matches, where dict[(i,j)] gives a list of a,b in i and c,d in j that have the same signature
    """
    rots, inverses = Transform.get_rotations()
    print("rotations")
    for i, rot in enumerate(rots):
        print(f"{i}: {rot.__str__(indent=4)}")
        
    rot_conversion = {} # rot_conversion[(i,j)] = rotation needed to convert from space i to space j
    point_mappings = {} # point_mappings[(i,j)] = dict where [a] = b gives the index of the points that correspond to each other
    
    for (i, j), pts in matches.items():
        print(f"comparing spaces {i} and {j}:")
        s1 = spaces[i]
        s2 = spaces[j]
        rot_ids = []
        point_mappings[(i,j)] = {}
        point_mappings[(j,i)] = {}
        
        for pt in pts:
            a = s1.points[pt[0]]
            b = s1.points[pt[1]]
            c = s2.points[pt[2]]
            d = s2.points[pt[3]]
            
            # note: because the order of points is arbitrary, either a->b corresponds to c->d or d->c
            # since mirror images are not superimposable, one will not be superimposable
            # find the superimposable one
            
            vi = minus(b, a)
            vj1 = minus(d, c)
            vj2 = minus(c, d)
            
            correct_rot_idx = None
            correct_rot = None
            
            for k, rot in enumerate(rots):
                result = rot.transform(vi)
                if result == vj1:
                    print(f"   found a valid transform from space {i}:[{pt[0]}->{pt[1]}]={vi} to {j}:[{pt[2]}->{pt[3]}]={vj1}: rot id = {i}")
                    correct_rot_idx = k
                    correct_rot = rot
                    point_mappings[(i,j)][pt[0]] = pt[2]
                    point_mappings[(i,j)][pt[1]] = pt[3]
                    point_mappings[(j,i)][pt[2]] = pt[0]
                    point_mappings[(j,i)][pt[3]] = pt[1]
                    break
                elif result == vj2:
                    print(f"   found a valid transform from space {i}:[{pt[0]}->{pt[1]}]={vi} to {j}:[{pt[3]}->{pt[2]}]={vj1}: rot id = {i}")
                    correct_rot_idx = k
                    correct_rot = rot
                    point_mappings[(i,j)][pt[0]] = pt[3]
                    point_mappings[(i,j)][pt[1]] = pt[2]
                    point_mappings[(j,i)][pt[3]] = pt[0]
                    point_mappings[(j,i)][pt[2]] = pt[1]
                    break
            if correct_rot_idx is None:
                print(f"   NO tranform found for space {i}:[{pt[0]}->{pt[1]}]={vi} to {j}:[{pt[3]}->{pt[2]}]={vj1}: rot id = {i}")
                continue
            rot_ids.append(correct_rot_idx)
            
        rot_id = mode(rot_ids)
        inv_rot_id = inverses[rot_id]
        rot_conversion[(i,j)] = rot_id
        rot_conversion[(j,i)] = inv_rot_id
        
    print(f"space rotation mappings: {sorted(rot_conversion.items())}")
        
    return rot_conversion, point_mappings, rots, inverses
        
def compute_offsets(spaces, rot_conversion, point_mappings, rotations):
    """
    spaces[i] = space i
    point_mappings = dict where (i,j) gives the dict of point mappings from space i to j, where dict[a] = b means a and b are the same point
    rot_conversion: dict where (i,j) gives the rotation idx of the rotation to convert from i to j
    rotations: list of rotations
    """
    for (i, j), rot_id in rot_conversion.items():
        rot = rotations[rot_id]
        
        offsets = []
        
        for a, b in point_mappings[(i,j)].items():
            # convert points from space i to space j, and then find the offset in space j
            # find offsets
            
            a_pt_i = spaces[i].points[a]
            b_pt_j = spaces[j].points[b]
            
            a_pt_j = rot.transform(a_pt_i)
            offset = minus(b_pt_j, a_pt_j)
            print(f"offset from {i}:[{a}]={a_pt_i} to {j}:[{b}]={b_pt_j} after rotating: {offset} ")
            offsets.append(offset)
            
        master_offset = [mode([offsets[x][y] for x in range(len(offsets))]) for y in range(len(offsets[0]))]
        
        translate = Transform.from_transform(dx=master_offset[0], dy=master_offset[1], dz=master_offset[2])
        master_transform = Transform.compound(translate, rot)
        spaces[i].relations[j] = master_transform
        
def find_path_to_0(spaces, rots, inverses):
    """walk through all spaces and ensure they have a valid transform to get to space 0"""
    
    spaces[0].relations[0] = Transform.identity()
    
    for i, s in reversed(list(enumerate(spaces))):
        print(f"checking space {i}:")
        if 0 in s.relations: # we can already reach space 0, no need to go further
            print(f"  * space 0 is already reachable from space {i}!")
            continue
            
        print(f"   cannot reach space 0 from space {i}")
            
       # begin walking
       # continue trying recursive neighbours until we find one path to 0
         
        visited = {}
        q = deque()
        q.append((i, Transform.identity()))
        found = False
        
        while len(q) > 0 and not found:
            j, T_ij = q.popleft() # A represents the transform from i to j
            if j in visited:
                continue
            visited[j] = True
            print(f"   walking to space {j}")
            
            # look at this space's neighbours
            for k, T_jk in spaces[j].relations.items():
                # find the transform from i to k by compounding i to j and j to k
                T_ik = Transform.compound(T_jk, T_ij)
                if k not in s.relations:
                    s.relations[k] = T_ik
                    print(f"     adding space mapping: {i}->{k}")
                    if k == 0: # target found!
                        print(f"  * 0 reached!")
                        found = True
                        break
                else: # have to keep walking
                    q.append((k, T_ik))
        
def count_points(spaces):
    points = {} # in 0 space
    
    for i, s in enumerate(spaces):
        for p in s.points:
            p = tuple(p)
            if i != 0:
                p = tuple(s.relations[0].transform(p))
            points[p] = True
    print(f"all beacons (relative to beacon 0): {sorted(points.keys())}")
    print(f"total number of points: {len(points)}")


scanners = read_input()
print(f"inputed {len(scanners)} scanners")

spaces = []
all_pairs = []
all_sigs = []
for i, scanner in enumerate(scanners):
    s = Space(points=scanner)
    spaces.append(s)
    print(f"scanner {i}:")
    pairs, sigs = s.calc_pair_fingerprints()
    all_pairs.append(pairs)
    all_sigs.append(sigs)
    
# find collisions
matches = find_matches(all_pairs, all_sigs)
rot_conversion, point_mappings, rots, inverses = compute_rotations(spaces, all_pairs, all_sigs, matches)
compute_offsets(spaces, rot_conversion, point_mappings, rots)

for i, s in enumerate(spaces):
    print(f"space {i} relations:")
    for j, r in s.relations.items():
        print(f" -> {j}: {r.__str__(indent=8)}")

find_path_to_0(spaces, rots, inverses)
count_points(spaces)