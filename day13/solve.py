#! /usr/bin/python3
import sys
import numpy


def parse_input(path):
    patterns = []
    for grid in open(path).read().split('\n\n'):
        rows = grid.strip().split('\n')
        pattern = numpy.zeros((len(rows), len(rows[0])), dtype=numpy.uint8)
        patterns.append(pattern)
        for y, row in enumerate(rows):
            for x, c in enumerate(row):
                if c == '#':
                    pattern[y, x] = 1
    return patterns


def fold(pattern, smudges):
    h, w = pattern.shape
    for x in range(1, w):
        l0, l1 = 0, x
        r0, r1 =  x - 1, w - 1
        delta = (l1 - l0) - (r1 - r0)
        if delta > 0:
            l0 += delta
        else:
            r1 += delta
        left = pattern[:, l0 : l1]
        right = pattern[:, r1 : r0 : -1]
        if numpy.sum(left != right) == smudges:
            return ('x', x)

    for y in range(1, h):
        u0, u1 = 0, y
        d0, d1 =  y - 1, h - 1
        delta = (u1 - u0) - (d1 - d0)
        if delta > 0:
            u0 += delta
        else:
            d1 += delta
        top = pattern[u0 : u1]
        bottom = pattern[d1 : d0 : -1]
        if numpy.sum(top != bottom) == smudges:
            return ('y', y)


def summarize(patterns, smudges):
    factor = {'x': 1, 'y': 100}
    total = 0
    for pattern in patterns:
        axis, count = fold(pattern, smudges)
        total += count * factor[axis]
    return total

 
def main(input_file):
    patterns = parse_input(input_file)
    print("Part 1:", summarize(patterns, smudges=0))
    print("Part 1:", summarize(patterns, smudges=1))


if __name__ == '__main__':
    main(sys.argv[1])
