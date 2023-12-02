# https://adventofcode.com/2021/day/1#part2


def bin_to_dec(bits):
    """bits = string array of 1 or 0 digits, big endian"""
    bits = bits[::-1]
    val = 0
    base = 1
    for i in range(len(bits)):
        digit = 1 if bits[i] == "1" else 0
        val += digit * base
        base *= 2
    return val
    
def filter_readings(readings, i, most_common):
    n = len(readings)
    counts = {}
    for b in [0, 1]:
        counts[b] = sum((1 for x in readings if x[i] == str(b)))
    counts = {k : v for k, v in counts.items() if v > 0} # filter out none entries
    
    keep = None
    extreme = None
    
    for b, count in counts.items():
        if extreme is None:
            keep = str(b)
            extreme = count
        elif most_common:
            if count > extreme or count == extreme and b == 1:
                keep = str(b)
                extreme = count
        elif not most_common:
            if count < extreme or count == extreme and b == 0:
                keep = str(b)
                extreme = count
    return [r for r in readings if r[i] == keep]
    
readings = []
n = -1

while True:
    try:
        bits = input() # big endian
        readings.append(bits)
        n = max(n, len(bits))
    except EOFError:
        break

        
# oxygen, most common, tiebreak towards 1
r = readings
o = None
for i in range(n):
    r = filter_readings(r, i, True)
    print("filtered", i, "remaining:", len(r))
    if len(r) == 1:
        o = bin_to_dec(r[0])
        break

# co2, least common, tiebreak towards 0
r = readings
c = None
for i in range(n):
    r = filter_readings(r, i, False)
    print("filtered", i, "remaining:", len(r))
    if (len(r) < 5): print(r)
    if len(r) == 1:
        c = bin_to_dec(r[0])
        break

print(o * c)
