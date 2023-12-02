def read_crabs():
    return [int(c) for c in input().split(",")]
    
def optimal(crabs):
    positions = sorted(crabs)
    xmin = positions[0]
    xmax = positions[-1]
    costs = {}
    x = xmin
    while x <= xmax:
        cost = 0
        for c in positions:
            cost += abs(c - x)
        costs[x] = cost
        x += 1
        
    return min(costs.items(), key=lambda x: x[1])

crabs = read_crabs()
print(crabs)

x, cost = optimal(crabs)
print(f"x = {x}, cost = {cost}")

