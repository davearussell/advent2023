#! /usr/bin/python3
import sys
import heapq

R, D, L, U = range(4)
MOVE = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def find_path(grid, min_line, max_line):
    start = (0, 0)
    h, w = len(grid), len(grid[0])
    goal = (w - 1, h - 1)
    frontier = []
    heapq.heappush(frontier, (0, start, None, 0))
    seen = set()
    while frontier:
        cost, pos, facing, n = heapq.heappop(frontier)
        for f2 in R, D, L, U:
            if f2 == facing and n == max_line:
                continue
            if facing is not None and (facing - f2) % 4 == 2:
                continue
            xo, yo = MOVE[f2]
            count = 1 if f2 == facing else min_line
            x2, y2 = pos
            if not (0 <= x2 + xo * count < w and 0 <= y2 + yo * count < h):
                continue
            c2 = cost
            for _ in range(count):
                x2, y2 = (x2 + xo, y2 + yo)
                c2 += int(grid[y2][x2])
            p2 = (x2, y2)
            n2 = n + count if f2 == facing else count
            if p2 == goal:
                return c2
            if (p2, f2, n2) not in seen:
                heapq.heappush(frontier, (c2, p2, f2, n2))
                seen.add((p2, f2, n2))
    assert 0, "unreachable"


def main(input_file):
    grid = open(input_file).read().strip().split('\n')
    print("Part 1:", find_path(grid, 1, 3))
    print("Part 2:", find_path(grid, 4, 10))


if __name__ == '__main__':
    main(sys.argv[1])
