#! /usr/bin/python3
import sys


def decode(value, digits):
    first = last = None
    for i in range(len(value)):
        for digit in digits:
            if value[i : i + len(digit)] == digit:
                if first is None:
                    first = digits[digit]
                last = digits[digit]
    return first * 10 + last


def main(input_file):
    values = open(input_file).read().split()
    digits = {str(d): d for d in range(1, 10)}
    print("Part 1:", sum(decode(value, digits) for value in values))
    digits.update({'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
                   'six': 6, 'seven': 7, 'eight': 8, 'nine': 9})
    print("Part 2:", sum(decode(value, digits) for value in values))


if __name__ == '__main__':
    main(sys.argv[1])
