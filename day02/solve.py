#! /usr/bin/python3
import re
import sys
from functools import reduce


def parse_input(path):
    games = []
    for i, line in enumerate(open(path)):
        game = {'id': i + 1, 'colors': {}}
        for n, color in re.findall(r'(\d+) (\w+)', line):
            game['colors'][color] = max(int(n), game['colors'].get(color, 0))
        games.append(game)
    return games


def possible(game, contents):
    return all(game['colors'][c] <= contents[c] for c in game['colors'])


def power(game):
    return reduce(int.__mul__, game['colors'].values())


def main(input_file):
    games = parse_input(input_file)
    contents = {'red': 12, 'green': 13, 'blue': 14}
    print("Part 1:", sum(g['id'] for g in games if possible(g, contents)))
    print("Part 2:", sum(power(game) for game in games))


if __name__ == '__main__':
    main(sys.argv[1])
