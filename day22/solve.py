#! /usr/bin/python3
import sys


def fall(bricks, update=False, without=None):
    n_fell = 0
    heights = {}
    for brick in bricks:
        if brick == without:
            continue
        (x0, y0, z0), (x1, y1, z1) = brick
        xys = [(x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)]
        height = max(heights.get(xy, 0) for xy in xys)
        drop = z0 - height - 1
        if drop:
            n_fell += 1
            z1 -= drop
            if update:
                brick[0][2] -= drop
                brick[1][2] -= drop
        for xy in xys:
            heights[xy] = z1
    return n_fell


def main(input_file):
    bricks = [[[int(x) for x in pos.split(',')] for pos in line.split('~')]
              for line in open(input_file).read().strip().split('\n')]
    bricks.sort(key=lambda b:b[0][2])
    fall(bricks, update=True)
    drop_counts = [fall(bricks, without=brick) for brick in bricks]
    print("Part 1:", drop_counts.count(0))
    print("Part 2:", sum(drop_counts))


if __name__ == '__main__':
    main(sys.argv[1])
