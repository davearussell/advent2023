#! /usr/bin/python3
import sys
import re


def xy_coefs(stone):
    """Returns coefficients A, B such that y = Ax + B."""
    x0, y0, _, X, Y, _ = stone
    A = Y / X
    t = -x0 / X # time at which x = 0
    B = y0 + t * Y
    return A, B


def xy_inter(s1, c1, s2, c2):
    """Returns the value of (x, y) at which y=A1x+B1 and y=A2x+B2 cross."""
    a1, b1 = c1
    a2, b2 = c2
    if a2 == a1:
        return None # parallel
    x = (b1 - b2) / (a2 - a1)
    for s in s1, s2:
        if (x - s[0]) / s[3] < 0:
            return None # intersection was in the past
    y = x * a1 + b1
    return x, y


def count_crosses(stones, lo, hi):
    coefs = [xy_coefs(stone) for stone in stones]
    n = 0
    for i in range(len(coefs)):
        for j in range(i + 1, len(coefs)):
            result = xy_inter(stones[i], coefs[i], stones[j], coefs[j])
            good = result is not None and lo <= min(result) <= max(result) <= hi
            if good:
                n += 1
    return n


def main(input_file):
    stones = []
    for line in open(input_file).read().strip().split('\n'):
        stones.append([int(x) for x in re.findall(r'[0-9-]+', line)])

    lo = 7 if len(stones) < 10 else 200000000000000
    hi = 27 if len(stones) < 10 else 400000000000000
    print("Part 1:", count_crosses(stones, lo, hi))




if __name__ == '__main__':
    main(sys.argv[1])
