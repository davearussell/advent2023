#! /usr/bin/python3
import sys
import numpy


def parse_input(path):
    lines = open(path).read().strip().split('\n')
    grid = numpy.zeros((len(lines), len(lines[0])), dtype=numpy.uint8)
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == '#':
                grid[y, x] = 1
            elif c == 'O':
                grid[y, x] = 2
    return grid


def load(grid):
    total = 0
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == 2:
                total += grid.shape[0] - y
    return total


def resolve(row):
    free = 0
    for pos, cell in enumerate(row):
        if cell == 1:
            free = pos + 1
        elif cell == 2:
            if pos > free:
                row[pos] = 0
                row[free] = 2
            free += 1


def tilt_up(grid):
    for x in range(grid.shape[1]):
        resolve(grid[:, x])


def cycle(grid):
    h, w = grid.shape
    for x in range(w):
        resolve(grid[:, x])
    for y in range(h):
        resolve(grid[y, :])
    for x in range(w):
        resolve(grid[::-1, x])
    for y in range(h):
        resolve(grid[y, ::-1])


def main(input_file):
    grid = parse_input(input_file)

    p1 = grid.copy()
    tilt_up(p1)
    print("Part 1:", load(p1))

    target = 1000000000
    seen = {}
    loads = []
    for i in range(target):
        b = grid.tobytes()
        if b in seen:
            a = seen[b]
            period = i - a
            rem = (target - a) % period
            print("Part 2:", loads[a + rem])
            break
        seen[b] = i
        loads.append(load(grid))
        cycle(grid)


if __name__ == '__main__':
    main(sys.argv[1])
