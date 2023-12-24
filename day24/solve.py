#! /usr/bin/python3
import sys
import re
from fractions import Fraction


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


def low_factors(n):
    return [i for i in range(2, 10000) if not n % i]


def possible_speeds(stones, axis):
    assert len(stones) == 2
    distance = stones[1][axis] - stones[0][axis]
    speed = stones[0][axis + 3]
    assert speed == stones[1][axis + 3]
    return {speed + x for factor in low_factors(distance) for x in [factor, -factor]}


def get_speed(by_vs, axis):
    speeds = None
    for k, stones in sorted(by_vs[axis].items()):
        if len(stones) == 2:
            if speeds is None:
                speeds = possible_speeds(stones, axis)
            else:
                speeds &= possible_speeds(stones, axis)
            assert len(speeds) >= 1
    assert len(speeds) == 1
    return speeds.pop()


def main(input_file):
    stones = []
    for line in open(input_file).read().strip().split('\n'):
        stones.append([int(x) for x in re.findall(r'[0-9-]+', line)])

    lo = 7 if len(stones) < 10 else 200000000000000
    hi = 27 if len(stones) < 10 else 400000000000000
    print("Part 1:", count_crosses(stones, lo, hi))

    by_vs = {}
    for stone in stones:
        for axis in range(3):
            v = stone[axis + 3]
            by_vs.setdefault(axis, {}).setdefault(v, []).append(stone)

    # I gave up on part 2 and copied this solution
    # https://www.reddit.com/r/adventofcode/comments/18pnycy/comment/keqf8uq/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
    RVX, RVY, RVZ = [get_speed(by_vs, axis) for axis in range(3)]
    APX, APY, APZ, AVX, AVY, AVZ = stones[0]
    BPX, BPY, BPZ, BVX, BVY, BVZ = stones[1]
    MA = Fraction(AVY-RVY, AVX-RVX)
    MB = Fraction(BVY-RVY, BVX-RVX)
    CA = APY - (MA*APX)
    CB = BPY - (MB*BPX)
    XPos = (CB-CA)/(MA-MB)
    YPos = MA*XPos + CA
    Time = (XPos - APX)//(AVX-RVX)
    ZPos = APZ + (AVZ - RVZ)*Time
    print("Part 2:", XPos + YPos + ZPos)

if __name__ == '__main__':
    main(sys.argv[1])
