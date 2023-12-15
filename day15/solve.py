#! /usr/bin/python3
import sys


def parse_input(path):
    steps = []
    for word in open(path).read().strip().split(','):
        op = '-' if '-' in word else '='
        if op == '=':
            label, lens = word.split(op)
            steps.append((word, label, int(lens)))
        else:
            label = word.rstrip(op)
            steps.append((word, label, None))
    return steps


def hash(text):
    h = 0
    for char in text:
        h = ((h + ord(char)) * 17) & 0xff
    return h


def power(boxes):
    total = 0
    for bi, (table, order) in enumerate(boxes):
        for li, label in enumerate(order):
            total += (bi + 1) * (li + 1) * table[label]
    return total


def main(input_file):
    steps = parse_input(input_file)
    print("Part 1:", sum(hash(word) for word, _, _ in steps))

    boxes = [({}, []) for _ in range(256)]
    for _, label, lens in steps:
        table, order = boxes[hash(label)]
        if lens is None:
            if label in table:
                del table[label]
                order.remove(label)
        else:
            if label not in table:
                order.append(label)
            table[label] = lens
    print("Part 2:", power(boxes))


if __name__ == '__main__':
    main(sys.argv[1])
