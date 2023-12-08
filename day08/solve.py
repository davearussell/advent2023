#! /usr/bin/python3
import math
import re
import sys


def parse_input(path):
    steps = None
    edges = {}

    for line in open(path):
        if steps is None:
            steps = [1 if c == 'R' else 0 for c in line.strip()]
        elif line.strip():
            src, left, right = re.match(r'(\w+) = .(\w+), (\w+).$', line).groups()
            edges[src] = [left, right]
    return steps, edges


def count_steps(steps, edges):
    at = 'AAA'
    n = 0
    while True:
        for step in steps:
            at = edges[at][step]
            n += 1
            if at == 'ZZZ':
                return n


def ghost_steps(steps, edges, at):
    # This function relies on the fact that all paths have been constructed
    # as cycles that will repeatedly hit the same Z node after
    # z0, z0 * 2, z0 * 3, ...etc steps. We go round the loop one more time
    # time after finding z0 to validate this.
    n = 0
    z = None
    count = None
    while True:
        for step in steps:
            at = edges[at][step]
            n += 1
            if at.endswith('Z'):
                assert n % len(steps) == 0
                if count is None:
                    count = n
                    z = at
                else:
                    assert z == at and count * 2 == n
                    return count
    return counts


def main(input_file):
    steps, edges = parse_input(input_file)
    print("Part 1:", count_steps(steps, edges))

    starts = [x for x in edges if x.endswith('A')]
    counts = [ghost_steps(steps, edges, at) for at in starts]
    print("Part 2:", math.lcm(*counts))


if __name__ == '__main__':
    main(sys.argv[1])
