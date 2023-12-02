from collections import deque

def read_paths():
    edges = {}
    while True:
        try:
            parts = input().split("-")
            if parts[0] not in edges:
                edges[parts[0]] = [parts[1]]
            else:
                edges[parts[0]].append(parts[1])
            if parts[1] not in edges:
                edges[parts[1]] = [parts[0]]
            else:
                edges[parts[1]].append(parts[0])
        except EOFError:
            break
    return edges
    
def walk(edges):
    logs = {} # string
    q = deque()
    q.append((False, ["start"])) # boolean = visited small
    while len(q) > 0:
        visited_small, path = q.popleft()
        choices = edges[path[-1]]
        # print(visited_small, path)
        for choice in choices:
            new_path = path + [choice]
            if choice == "end":
                logs[",".join(new_path)] = True
            elif choice == "start":
                continue
            elif choice.islower() and choice in path: # cannot revisit lowercase
                if not visited_small:
                    q.append((True, new_path))
                else:
                    continue
            else:
                # visit node
                q.append((visited_small, new_path))
    print(logs)
    print(len(logs))
    
edges = read_paths()
print(edges)
walk(edges)
