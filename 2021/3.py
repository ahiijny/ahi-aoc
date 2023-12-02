# https://adventofcode.com/2021/day/1#part2


def bin_to_dec(bits):
    """bits = string array of 1 or 0 digits, little endian"""
    val = 0
    base = 1
    for i in range(len(bits)):
        digit = 1 if bits[i] == "1" else 0
        val += digit * base
        base *= 2
    return val

ones = []
zeroes = []

while True:
    try:
        bits = input()[::-1] # little endian
        if len(ones) < len(bits):
            ones.extend([0] * ((len(bits) - len(ones))))
            zeroes.extend([0] * ((len(bits) - len(zeroes))))
        for i, b in enumerate(bits):
            if b == "1":
                ones[i] += 1
            else:
                zeroes[i] += 1
    except EOFError:
        break

y = []
e = []

for i in range(len(ones)):
    if ones[i] > zeroes[i]:
        y.append("1")
        e.append("0")
    else:
        y.append("0")
        e.append("1")

y10 = bin_to_dec(y)
e10 = bin_to_dec(e)     
        
print(y10 * e10)
