#! /usr/bin/python3
import sys

PIPES = {
    '|': [(0, -1), (0, 1)],
    '-': [(-1, 0), (1, 0)],
    'L': [(0, -1), (1, 0)],
    'J': [(0, -1), (-1, 0)],
    '7': [(0, 1), (-1, 0)],
    'F': [(0, 1), (1, 0)],
}


def parse_input(path):
    grid = {}
    edges = {}
    start = None
    # Populate the grid
    for y, line in enumerate(open(path)):
        for x, c in enumerate(line.strip()):
            grid[(x, y)] = c
            if c == 'S':
                start = (x, y)

    # Find the edges
    edges = find_edges(grid)
    for src in list(edges):
        if start in edges[src]:
            edges.setdefault(start, []).append(src)

    # Work out what pipe type start must be
    x, y = start
    if (x - 1, y) in edges[start] and (x + 1, y) in edges[start]:
        grid[start] = '-'
    if (x, y - 1) in edges[start] and (x, y + 1) in edges[start]:
        grid[start] = '|'
    if (x - 1, y) in edges[start] and (x, y + 1) in edges[start]:
        grid[start] = 'L'
    if (x, y - 1) in edges[start] and (x - 1, y) in edges[start]:
        grid[start] = 'J'
    if (x, y + 1) in edges[start] and (x - 1, y) in edges[start]:
        grid[start] = '7'
    if (x, y + 1) in edges[start] and (x + 1, y) in edges[start]:
        grid[start] = 'F'

    return grid, edges, start


def find_edges(grid):
    edges = {}
    for (x, y), cell in grid.items():
        if cell in PIPES:
            edges[(x, y)] = [(x + xo, y + yo) for xo, yo in PIPES[cell]]
    return edges


def print_grid(grid, loop, outside):
    x1 = max(x for (x, y) in grid)
    y1 = max(y for (x, y) in grid)
    lines = {'|': '┃', '-': '━', 'L': '┗', 'F': '┏', 'J': '┛', '7': '┓'}
    s = ''
    def c(s, col):
        cols = {'r': 31, 'g': 32, 'y': 33, 'b': 34}
        return '\x1b[%dm%s\x1b[0m' % (cols[col], s)
    for y in range(y1 + 1):
        for x in range(x1 + 1):
            pos = (x, y)
            if pos in loop:
                s += c(lines.get(grid[pos], '?'), 'b')
            elif pos in outside:
                s += c('.', 'g')
            elif grid[pos] == 'X':
                s += ' '
            else:
                s += c('#', 'r')
        s += '\n'
    print(s)


def find_loop(edges, start):
    prev = start
    at = edges[start][0]
    loop = {at}
    while at != start:
        at, prev = [x for x in edges[at] if x != prev][0], at
        loop.add(at)
    return loop


def widen_grid(grid, loop):
    new_grid = {}
    x1 = max(x for (x, y) in grid)
    y1 = max(y for (x, y) in grid)

    for y in range(y1 + 1):
        for x in range(x1 + 1):
            cell = grid[(x, y)]
            new_grid[(x * 2, y * 2)] = cell
            new_grid[(x * 2 + 1, y * 2)] = '-' if cell in '-FL' and (x, y) in loop else 'X'
            new_grid[(x * 2, y * 2 + 1)] = '|' if cell in '7|F' and (x, y) in loop else 'X'
            new_grid[(x * 2 + 1, y * 2 + 1)] = 'X'
    return new_grid


def find_outside(grid, loop):
    assert (0, 0) not in loop
    outside = set()
    x1 = max(x for (x, y) in grid)
    y1 = max(y for (x, y) in grid)

    def neighbours(pos):
        x, y = pos
        n = set()
        for xo, yo in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            xn, yn = x + xo, y + yo
            if -1 <= xn <= x1 + 1 and -1 <= yn <= y1 + 1 and (xn, yn) not in loop:
                n.add((xn, yn))
        return n

    frontier = {(0, 0)}
    while frontier:
        new_frontier = set()
        for pos in frontier:
            outside.add(pos)
            new_frontier |= neighbours(pos)
        frontier = new_frontier - outside

    return outside


def main(input_file):
    grid, edges, start = parse_input(input_file)
    loop = find_loop(edges, start)
    print("Part 1:", len(loop) // 2)

    outside = find_outside(grid, loop)
    print_grid(grid, loop, outside)

    new_grid = widen_grid(grid, loop)
    new_edges = find_edges(new_grid)
    new_start = (start[0] * 2, start[1] * 2)
    new_loop = find_loop(new_edges, new_start)
    new_outside = find_outside(new_grid, new_loop)
    new_inside = [pos for pos in new_grid
                  if pos not in new_loop
                  and pos not in new_outside
                  and new_grid[pos] != 'X']
    print()
    print_grid(new_grid, new_loop, new_outside)
    print("Part 2:", len(new_inside))

    # 819: HI

if __name__ == '__main__':
    main(sys.argv[1])
