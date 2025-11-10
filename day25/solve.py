#! /usr/bin/python3
import copy
import pprint
import sys


def parse_input(path):
    conns = {}
    for line in open(path):
        parts = line.replace(':', '').split()
        lhs, rhs = parts[0], parts[1:]
        l = conns.setdefault(lhs, [])
        l += rhs
        for part in rhs:
            conns.setdefault(part, []).append(lhs)
    return conns


def shortest_paths(start, conns):
    paths = {}
    todo = set(conns)
    frontier = [(start,)]
    while frontier:
        new_frontier = []
        todo -= {path[-1] for path in frontier}
        for path in frontier:
            dst = path[-1]
            paths[dst] = path
            new_frontier += [path + (part,) for part in conns[dst] if part in todo]
        frontier = new_frontier
    return paths


def cut_wires(conns, wires):
    conns = copy.deepcopy(conns)
    for a, b in wires:
        conns[a].remove(b)
        conns[b].remove(a)
    return conns


def find_connecting_wires(conns):
    freqs = {}
    for i, part in enumerate(conns):
        paths = shortest_paths(part, conns)
        for dst, path in paths.items():
            for a, b in zip(path, path[1:]):
                k = (b, a) if a > b else (a, b)
                freqs[k] = freqs.get(k, 0) + 1
        most_used_wires = [x[0] for x in sorted(freqs.items(), key=lambda x: -x[1])[:3]]
        reachable = shortest_paths(part, cut_wires(conns, most_used_wires))
        if len(reachable) < len(conns):
            return most_used_wires, len(reachable)


def main(input_file):
    conns = parse_input(input_file)
    connecting_wires, group_size = find_connecting_wires(conns)
    print(group_size * (len(conns) - group_size))



if __name__ == '__main__':
    main(sys.argv[1])
