#! /usr/bin/python3
import math
import sys
from functools import reduce


def parse_input(path):
    races = []
    for line in open(path):
        words = line.split()
        for i, word in enumerate(line.split()[1:]):
            word = int(word)
            if i >= len(races):
                races.append([word])
            else:
                races[i].append(word)
    return races


def count_strategies(duration, distance):
    # The button time at which we match the record can be expressed as
    #   -button_time^2 + duration*button_time - distance = 0
    # Apply the quadratic formula to solve
    # We only find the lower solution as we know the two solutions sum to duration
    button_time = (duration - (duration ** 2 - 4 * distance) ** .5) / 2

    # The minimum time to win is the smallest integer > button_time
    button_time = math.ceil(button_time)
    if button_time * (duration - button_time) == distance:
        button_time += 1

    return (duration - button_time) - button_time + 1


def main(input_file):
    races = parse_input(input_file)
    button_times = [count_strategies(*race) for race in races]
    print("Part 1:", reduce(int.__mul__, button_times))

    p2_duration = int(reduce(str.__add__, [str(dur) for dur, dist in races]))
    p2_distance = int(reduce(str.__add__, [str(dist) for dur, dist in races]))
    print("Part 2:", count_strategies(p2_duration, p2_distance))


if __name__ == '__main__':
    main(sys.argv[1])


