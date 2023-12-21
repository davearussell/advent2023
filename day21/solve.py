#! /usr/bin/python3
import sys


def unreachable(plots):
    for x, y in plots:
        neighbours = {(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)}
        if not plots & neighbours:
            yield (x, y)


def parse_input(path):
    plots = set()
    for y, line in enumerate(open(path).read().strip().split('\n')):
        for x, c in enumerate(line):
            if c == 'S':
                start = (x, y)
                plots.add((x, y))
            elif c == '.':
                plots.add((x, y))
    return start, plots - set(unreachable(plots))


def explore(start, plots, limit=0):
    x1 = max(x for x, y in plots)
    y1 = max(y for x, y in plots)
    at = {start}
    reachable = [] # n_steps -> n_plots
    while True:
        if limit:
            print("%d steps: %d plots" % (len(reachable), len(at)))
            if len(reachable) == limit:
                return reachable
        reachable.append(len(at))
        if sum(reachable[-2:]) == len(plots):
            return reachable
        new_at = set()
        for pos in at:
            x, y = pos
            new_at |= {(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)}
        at = new_at & plots


def all_plot_counts(plots):
    # Assumptions:
    # 1. The grid is square
    # 2. The start point is always dead centre (also requires grid length is odd)
    # 3. There is a clear straight line from center to each edge, and between adjacent corners
    #
    # With these, we will always enter a new grid at either a corner or the center of an edge,
    # so we can precompute the reachable plot counts starting from these points
    #
    # NOTE: these assumptions are NOT true of the example input
    l = min(x for x, y in plots)
    t = min(x for x, y in plots)
    r = max(x for x, y in plots)
    b = max(y for x, y in plots)
    assert l == t == 0
    assert r == b and not r & 1
    m = r // 2
    to_try = [
        (m, m), # centre
        (l, t), # top left
        (m, t), # top middle
        (r, t), # top right
        (r, m), # middle right
        (r, b), # bottom right
        (m, b), # bottom middle
        (l, b), # bottom left
        (l, m), # middle left
    ]
    return {pos: explore(pos, plots) for pos in to_try}, r + 1


def reachable_plots(counts, length, steps):
    half = length // 2
    initial_counts = counts[(half, half)]
    cardinal_counts = [cc for pos, cc in counts.items() if pos.count(half) == 1]
    diagonal_counts = [cc for pos, cc in counts.items() if pos.count(half) == 0]
    max_c, c_steps = divmod(steps + half, length)
    max_d, d_steps = divmod(steps - 1, length)
    i_steps_max = len(initial_counts) - 1
    c_steps_max = len(cardinal_counts[0]) - 1
    d_steps_max = len(diagonal_counts[0]) - 1

    print("%d steps:" % (steps,))

    i = -2 if (steps ^ i_steps_max) & 1 else -1
    total_reachable = initial_counts[i]
    print("  (0, 0): reachable=%d" % (total_reachable,))

    while max_c and c_steps < c_steps_max:
        reachable = [cc[c_steps] for cc in cardinal_counts]
        print("  (%d, 0): steps=%d reachable=%d   %r" % (max_c, c_steps, sum(reachable), reachable))
        total_reachable += sum(reachable)
        max_c -= 1
        c_steps += length
    n_even = max_c // 2
    n_odd = max_c - n_even
    odd_i = -2 if ((steps - half - 1) ^ c_steps_max) & 1 else -1
    even_i = -2 if odd_i == -1 else -1
    if n_odd:
        odd_reachable = cardinal_counts[0][odd_i]
        odd_grids = n_odd * 4
        print("  (odd, 0): reachable=%d   [%d * %d]" % (
            odd_reachable * odd_grids, odd_reachable, odd_grids))
        total_reachable += odd_reachable * odd_grids
    if n_even:
        even_reachable = cardinal_counts[0][even_i]
        even_grids = n_even * 4
        print("  (even, 0): reachable=%d   [%d * %d]" % (
            even_reachable * even_grids, even_reachable, even_grids))
        total_reachable += even_reachable * even_grids

    d_steps_max = len(diagonal_counts[0]) - 1
    while max_d and d_steps < d_steps_max:
        reachable = [dc[d_steps] for dc in diagonal_counts]
        print("  (%d, 1): steps=%d reachable=%d   %r * %d" % (
            max_d, d_steps, sum(reachable) * max_d, reachable, max_d))
        total_reachable += sum(reachable) * max_d
        max_d -= 1
        d_steps += length
    n_even = max_d // 2
    n_odd = max_d - n_even
    odd_i = -2 if ((steps - 2 * half - 2) ^ d_steps_max) & 1 else -1
    even_i = -2 if odd_i == -1 else -1
    if n_odd:
        odd_reachable = diagonal_counts[0][odd_i]
        odd_grids = n_odd * n_odd * 4
        print("  (odd, 1): reachable=%d   [%d * %d]" % (
            odd_reachable * odd_grids, odd_reachable, odd_grids))
        total_reachable += odd_reachable * odd_grids
    if n_even:
        even_reachable = diagonal_counts[0][even_i]
        even_grids = n_even * (n_even + 1) * 4
        print("  (even, 1): reachable=%d   [%d * %d]" % (
            even_reachable * even_grids, even_reachable, even_grids))
        total_reachable += even_reachable * even_grids

    return total_reachable


def main(input_file):
    start, plots = parse_input(input_file)
    counts, length = all_plot_counts(plots)
    print("Part 1:", counts[start][64])
    print("Part 2:", reachable_plots(counts, length, 26501365))


if __name__ == '__main__':
    main(sys.argv[1])
