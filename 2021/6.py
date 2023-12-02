def read_fish():
    return [int(i) for i in input().split(",")]
    
def sim(fish, days):
    birthing = []
    for d in range(days):
        birthing = []
        for i in range(len(fish)):
            fish[i] -= 1
            if fish[i] < 0:
                fish[i] = 6
                birthing.append(8)
        fish.extend(birthing)
    return fish
                
    
fish = read_fish()
new_fish = sim(fish, 80)
print(len(new_fish))
