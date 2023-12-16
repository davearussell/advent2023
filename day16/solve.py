#! /usr/bin/python3
import sys

R, D, L, U = range(4)
MOVE = [(1, 0), (0, 1), (-1, 0), (0, -1)]
TURN = {
    '.': [[R], [D], [L], [U]],
    '/': [[U], [L], [D], [R]],
    '\\': [[D], [R], [U], [L]],
    '|': [[U, D], [D], [U, D], [U]],
    '-': [[R], [L, R], [L], [L, R]],
}


def trace_beam(grid, pos, facing):
    beams = {(pos, facing)} # { ((x, y), facing), ... }
    h, w = len(grid), len(grid[0])
    lit = set()
    seen = set()
    while beams:
        new_beams = set()
        for (x, y), facing in beams:
            xo, yo = MOVE[facing]
            x, y = x + xo, y + yo
            if not (0 <= x < w and 0 <= y < h):
                continue
            lit.add((x, y))
            for facing in TURN[grid[y][x]][facing]:
                k = ((x, y), facing)
                if k not in seen:
                    new_beams.add(k)
                    seen.add(k)
        beams = new_beams
    return len(lit)


def all_starts(grid):
    h, w = len(grid), len(grid[0])
    for y in range(h):
        yield (-1, y), R
        yield (w, y), L
    for x in range(w):
        yield (x, -1), D
        yield (x, y), U


def main(input_file):
    grid = open(input_file).read().strip().split('\n')
    print("Part 1:", trace_beam(grid, (-1, 0), R))
    print("Part 2:", max(trace_beam(grid, pos, facing) for pos, facing in all_starts(grid)))


if __name__ == '__main__':
    main(sys.argv[1])
