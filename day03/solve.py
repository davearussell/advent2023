#! /usr/bin/python3
import sys


def parse_input(path):
    numbers = {}
    symbols = {}
    current_number = None
    for y, line in enumerate(open(path).read().strip().split('\n')):
        for x, char in enumerate(line):
            if char.isdigit():
                if current_number:
                    numbers[current_number] += char
                else:
                    current_number = (x, y)
                    numbers[(x, y)] = char
            else:
                current_number = None
                if char != '.':
                    symbols[(x, y)] = char
    return numbers, symbols


def neighbouring_symbols(x0, x1, y, symbols):
    neighbours = {(x, y_) for x in range(x0 - 1, x1 + 2) for y_ in range(y - 1, y + 2)}
    return neighbours & symbols


def get_p2s(numbers, symbols):
    p2s = {}
    for (x, y), number in numbers.items():
        p2s[(x, y)] = neighbouring_symbols(x, x + len(number) - 1, y, symbols)
    return p2s # Maps number positions to set of neighbouring symbol positions


def get_s2p(p2s):
    s2p = {}
    for p_pos, s_poses in p2s.items():
        for s_pos in s_poses:
            s2p.setdefault(s_pos, set()).add(p_pos)
    return s2p # Maps symbol positions to set of neighbouring number positions


def sum_parts(p2s, numbers):
    return sum(int(n) for pos, n in numbers.items() if p2s.get(pos))


def sum_gears(p2s, numbers, symbols):
    total = 0
    for s_pos, p_poses in get_s2p(p2s).items():
        if len(p_poses) == 2 and symbols[s_pos] == '*':
            total += int(numbers[p_poses.pop()]) * int(numbers[p_poses.pop()])
    return total


def main(input_file):
    numbers, symbols = parse_input(input_file)
    p2s = get_p2s(numbers, set(symbols))
    print("Part 1:", sum_parts(p2s, numbers))
    print("Part 2:", sum_gears(p2s, numbers, symbols))


if __name__ == '__main__':
    main(sys.argv[1])
