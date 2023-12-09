#! /usr/bin/python3
import sys
from functools import reduce


def parse_input(path):
    return [[int(x) for x in line.split()]
            for line in open(path).read().strip().split('\n')]


def extend(seq):
    seqs = [seq]
    while any(seqs[-1]):
        seqs.append([b - a for (a, b) in zip(seqs[-1], seqs[-1][1:])])
    prev = reduce(lambda a, b: b - a, [seq[0] for seq in seqs[::-1]])
    succ = sum(seq[-1] for seq in seqs)
    return [prev] + seq + [succ]


def main(input_file):
    histories = parse_input(input_file)
    extended = [extend(history) for history in histories]
    print("Part 1:", sum(e[-1] for e in extended))
    print("Part 2:", sum(e[0] for e in extended))


if __name__ == '__main__':
    main(sys.argv[1])
