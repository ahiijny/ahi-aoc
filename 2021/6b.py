def read_fish():
    return [int(i) for i in input().split(",")]

    
def sim(fish, days):
    census = [0] * 9 # census[age] = count
    for age in fish:
        census[age] += 1
        
    for d in range(days):
        next_census = [0] * 9
        for i in range(len(census)):
            if i == 0:
                next_census[6] += census[0]
            else:
                next_census[i-1] += census[i]
        next_census[8] += census[0]
        census = next_census
    return census
     
    
fish = read_fish()
census = sim(fish, 256)
total = sum(census)
print(total)
