#! /usr/bin/python3
import sys


SLOPES = {'>': (1, 0), '<': (-1, 0), '^': (0, -1), 'v': (0, 1)}
def parse_input(path):
    paths = set()
    slopes = {}
    for y, line in enumerate(open(path).read().strip().split('\n')):
        for x, c in enumerate(line):
            if c != '#':
                paths.add((x, y))
                if c != '.':
                    slopes[(x, y)] = SLOPES[c]
    return paths, slopes


def follow_path(pos, next_step, paths):
    distance = 0
    while True:
        distance += 1
        x, y = next_step
        next_steps = {(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)} & paths - {pos}
        if len(next_steps) != 1:
            return distance, next_step, pos, next_steps
        pos, next_step = next_step, next_steps.pop()


def make_graph(paths, slopes, start, goal):
    graph = {start: {}, goal: {}}

    tried = set()
    frontier = {(start, (start[0], start[1] + 1))}
    while frontier:
        new_frontier = set()
        for pos, first_step in frontier:
            dist, new_pos, last_step, next_steps = follow_path(pos, first_step, paths)
            if slopes:
                next_steps = [step for step in next_steps
                              if slopes[step] == (step[0] - new_pos[0], step[1] - new_pos[1])]
            graph.setdefault(pos, {})[new_pos] = dist
            if not slopes:
                graph.setdefault(new_pos, {})[pos] = dist
            for step in next_steps:
                if step not in tried:
                    tried.add(step)
                    new_frontier.add((new_pos, step))
        frontier = new_frontier
    return graph


def longest_walk(graph, start, goal):
    walks = [([start], 0)]
    best = 0
    while walks:
        new_walks = []
        for path, dist in walks:
            if goal in graph[path[-1]]:
                length = dist + graph[path[-1]][goal]
                if length > best:
                    best = length
                continue
            for next_pos, next_dist in graph[path[-1]].items():
                if next_pos not in path:
                    new_walks.append((path + [next_pos], dist + next_dist))
        walks = new_walks
    return best


def main(input_file):
    paths, slopes = parse_input(input_file)
    start = (min(x for x, y in paths), min(y for x, y in paths))
    goal = (max(x for x, y in paths), max(y for x, y in paths))

    p1_graph = make_graph(paths, slopes, start, goal)
    print("Part 1:", longest_walk(p1_graph, start, goal))

    p2_graph = make_graph(paths, None, start, goal)
    print("Part 2:", longest_walk(p2_graph, start, goal))


if __name__ == '__main__':
    main(sys.argv[1])
