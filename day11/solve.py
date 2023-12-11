#! /usr/bin/python3
import sys


def explode(galaxies, factor):
    xs = {x for x, y in galaxies}
    ys = {y for x, y in galaxies}
    empty_x = set(range(max(xs) + 1)) - xs
    empty_y = set(range(max(ys) + 1)) - ys
    new_galaxies = set()
    for x, y in galaxies:
        x += len([_x for _x in empty_x if _x < x]) * (factor - 1)
        y += len([_y for _y in empty_y if _y < y]) * (factor - 1)
        new_galaxies.add((x, y))
    return new_galaxies


def shortest_paths(galaxies):
    return sum(abs(x2 - x1) + abs(y2 - y1)
               for (x1, y1) in galaxies for (x2, y2) in galaxies
               if (x2, y2) > (x1, y1))


def main(input_file):
    galaxies = {(x, y) for (y, line) in enumerate(open(input_file))
                for (x, char) in enumerate(line.strip())
                if char == '#'}
    print("Part 1:", shortest_paths(explode(galaxies, 2)))
    print("Part 2:", shortest_paths(explode(galaxies, 1000000)))


if __name__ == '__main__':
    main(sys.argv[1])
