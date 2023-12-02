import numpy as np

def mix(numbers, times):
    for _ in range(times):
        to_mix = 0
        while to_mix < length:
            index = -1
            for i in range(length):
                if numbers[i][1] == to_mix:
                    index = i
                    to_mix += 1
                    break

            num = (abs(numbers[index][0]) % (length - 1)) * np.sign(numbers[index][0])

            if index + num >= length - 1 or index + num <= 0:
                new_index = (index + num + np.sign(num) + length) % length
            else:
                new_index = index + num

            numbers.insert(new_index, numbers.pop(index))
    return [num[0] for num in numbers]

with open("input.txt", "r") as f:
    lines = [line.rstrip() for line in f]
    length = len(lines)
    part_1 = [(int(lines[i]), i) for i in range(length)]
    part_2 = [(int(lines[i]) * 811589153, i) for i in range(length)]

    part_1 = mix(part_1, 1)
    idx = part_1.index(0)
    print(f"part 1: {sum([part_1[(1000 + idx) % length], part_1[(2000 + idx) % length], part_1[(3000 + idx) % length]])}")

    part_2 = mix(part_2, 10)
    idx = part_2.index(0)
    print(f"part 2: {sum([part_2[(1000 + idx) % length], part_2[(2000 + idx) % length], part_2[(3000 + idx) % length]])}")
