#! /usr/bin/python3
import sys


def parse_input(path):
    seeds = None
    maps = []
    for line in open(path):
        if line.startswith('seeds:'):
            seeds = [int(word) for word in line.split()[1:]]
        elif ':' in line:
            maps.append([])
        elif line.strip():
            maps[-1].append([int(word) for word in line.split()])
    return seeds, maps


def lookup(v, map_):
    next_range = None
    for dst, src, n in map_:
        offset = v - src
        if offset >= 0 and (n is None or offset < n):
            return dst + offset, None if n is None else n - offset
        elif offset < 0 and (next_range is None or next_range > -offset):
                next_range = -offset
    return v, next_range


def fill_gaps(map_):
    map_out = []
    v = 0
    for i, (dst, src, n) in enumerate(sorted(map_, key=lambda m: m[1])):
        if src > v:
            map_out.insert(i, (v, v, (src - v)))
        map_out.append((dst, src, n))
        if n is not None:
            v = src + n
    map_out.append((v, v, None))
    return map_out


def merge_two_maps(map1, map2):
    map_out = []

    map1 = fill_gaps(map1)
    map2 = fill_gaps(map2)

    r2, r1, n1 = map1.pop(0)
    while True:
        r3, n2 = lookup(r2, map2)
        if n1 is None or n2 is None:
            n = n1 or n2
        else:
            n = min(n1, n2)
        map_out.append((r3, r1, n))
        if n is None:
            return map_out
        if n == n1:
            r2, r1, n1 = map1.pop(0)
        else:
            r2 += n
            r1 += n
            if n1 is not None:
                assert n < n1
                n1 -= n


def merge_maps(maps):
    while len(maps) > 1:
        maps = [merge_two_maps(maps[0], maps[1])] + maps[2:]
    return maps[0]


def best_location(seed_ranges, the_map):
    best = None
    while seed_ranges:
        seed = seed_ranges.pop(0)
        sn = seed_ranges.pop(0)
        while True:
            loc, ln = lookup(seed, the_map)
            if best is None or loc < best:
                best = loc
            if ln >= sn:
                break
            seed += ln
            sn -= ln
    return best


def main(input_file):
    seeds, maps = parse_input(input_file)
    the_map = merge_maps(maps)
    print("Part 1:", min(lookup(seed, the_map)[0] for seed in seeds))
    print("Part 2:", best_location(seeds, the_map))


if __name__ == '__main__':
    main(sys.argv[1])
