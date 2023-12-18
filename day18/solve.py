#! /usr/bin/python3
import re
import sys

MOVE = [(1, 0), (0, 1), (-1, 0), (0, -1)]


def parse_input(path):
    steps1 = []
    steps2 = []
    pat = re.compile(r'([UDLR]) (\d+) .#(.+).')
    for line in open(path).read().strip().split('\n'):
        f1, n1, code = pat.match(line).groups()
        n2, f2 = code[:-1], code[-1]
        steps1.append(('RDLU'.index(f1), int(n1)))
        steps2.append((int(f2), int(n2, base=16)))
    return draw_lines(steps1), draw_lines(steps2)


def draw_lines(steps):
    lines = []
    x = y = 0
    for facing, n in steps:
        xo, yo = MOVE[facing]
        x0, y0 = x, y
        x, y = x + xo * n, y + yo * n
        a, b = (x0, y0), (x, y)
        if a > b:
            a, b = b, a
        lines.append((a, b))
    return lines


def next_verticals(line, lines):
    (x, top), (x1, bottom) = line
    found = None
    matches = []
    for line2 in lines:
        (x0, y0), (x1, y1) = line2
        if found is not None and x0 > found:
            break
        if x < x0 == x1:
            if y0 <= bottom and y1 >= top:
                matches.append((y0, y1))
                found = x0
    return found, matches


def fill_lines(lines):
    area = 0
    n = len(lines)
    todo = sorted(lines)
    while todo:
        vert = todo.pop(0)
        top_horiz = [l for l in todo if l[0] == vert[0] and l != vert][0]
        bot_horiz = [l for l in todo if l[0] == vert[1]][0]
        (x, top), (_, bottom) = vert
        rhs, next_verts = next_verticals(vert, todo)

        for horiz in [top_horiz, bot_horiz]:
            (x0, y0), (x1, y1) = horiz
            todo.remove(horiz)
            if x1 > rhs:
                todo.append(((rhs, y0), (x1, y1)))

        new_area = 0
        new_verts = [[top, bottom]]
        for y0, y1 in next_verts:
            nvert = (rhs, y0), (rhs, y1)
            todo.remove(nvert)
            if y1 == top:
                new_verts[0][0] = y0
            elif y0 == bottom:
                new_verts[-1][1] = y1
            else:
                new_area += y1 - y0 - 1
                if y0 == top:
                    new_area += 1
                if y1 == bottom:
                    new_area += 1

                new_new_verts = []
                for v0, v1 in new_verts:
                    if v0 == y0:
                        if v1 > y1:
                            new_new_verts.append([y1, v1])
                    elif y0 > v1:
                        new_new_verts.append([v0, v1])
                    else:
                        if y1 < v1:
                            new_new_verts.append([v0, y0])
                            new_new_verts.append([y1, v1])
                        else:
                            new_new_verts.append([v0, y0])
                new_verts = new_new_verts

        new_area += (bottom - top + 1) * (rhs - x)
        area += new_area
        for y0, y1 in new_verts:
            new_line = ((rhs, y0), (rhs, y1))
            todo.append(new_line)
        todo.sort()

    return area


def main(input_file):
    lines1, lines2 = parse_input(input_file)
    print("Part 1:", fill_lines(lines1))
    print("Part 2:", fill_lines(lines2))


if __name__ == '__main__':
    main(sys.argv[1])
