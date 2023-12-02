def read_input():
    alg = []
    img = []
    
    try:
        alg = input()
        input()
        while True:
            img.append(input())
    except EOFError:
        pass
        
    return alg, img
    
def btoi(bits): # big endian
    x = 0
    for d in bits:
        x *= 2
        x += d
    return x
    
def pad(img, amount):
    # add 12 to top, left, right, bottom
    # assume that all 0s for input will result in 0 output
    img2 = [["." for c in range(len(img[0]) + 2*amount)] for r in range(len(img) + 2*amount)]
    for r in range(len(img)):
        for c in range(len(img[0])):
            img2[r+amount][c+amount] = img[r][c]
    return img2
    
def trim(img):
    # to remove edge artifacts
    img2 = [["." for c in range(len(img[0]) - 2)] for r in range(len(img) - 2)]
    for r in range(1, len(img)-1):
        for c in range(1, len(img[0])-1):
            img2[r-1][c-1] = img[r][c]
    return img2
    
    
def kernel(alg, img, r, c):
    bits = []
    for r2 in range(r-1, r+2):
        for c2 in range(c-1, c+2):
            bit = 0
            if 0 <= r2 and r2 < len(img):
                if 0 <= c2 and c2 < len(img[0]):
                    bit = img[r2][c2] == "#"
            bits.append(bit)
    value = btoi(bits)
    on = alg[value] == '#'
    return on
    
def enhance(alg, img):
    result = [[None for c in range(len(img[0]))] for r in range(len(img))]
    for r in range(len(img)):
        for c in range(len(img[0])):
            on = kernel(alg, img, r, c)
            result[r][c] = "#" if on else "."
    result = trim(result)
    return result
    
def count_on(img):
    count = 0
    for r in range(len(img)):
        for c in range(len(img[r])):
            if img[r][c] == "#":
                count += 1
    return count
    
def printimg(img):
    for r in img:
        print(''.join(r))
        
alg, img = read_input()
print(alg)
print(img)

img = pad(img, 104)
print("original image:")
printimg(img)

for i in range(50):
    img = enhance(alg, img)
    print("enhance " + str(i))

print("final image:")
printimg(img)
print(count_on(img))