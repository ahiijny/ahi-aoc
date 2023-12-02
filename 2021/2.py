# https://adventofcode.com/2021/day/1#part2

x = 0
depth = 0

while True:
    try:
        move = input().split()
        command = move[0]
        amount = int(move[1])
        
        if command == "forward":
            x += amount
        elif command == "down":
            depth += amount
        elif command == "up":
            depth -= amount
    except EOFError:
        break
        
print(x * depth)
