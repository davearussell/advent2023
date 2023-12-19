#! /usr/bin/python3
import re
import sys
from functools import reduce


rule_pat = re.compile(r'([a-z]+)(.)(\d+):(.+)')
def parse_input(path):
    workflows = {}
    parts = []

    for line in open(path).read().strip().split('\n'):
        if ':' in line:
            workflow = {'rules': []}
            workflow['name'], rules_s = line.rstrip('}').split('{')
            rules = []
            for rule_s in rules_s.split(','):
                if ':' in rule_s:
                    key, op, val, target = rule_pat.search(rule_s).groups()
                    workflow['rules'].append(((key, op, int(val)), target))
                else:
                    workflow['rules'].append((None, rule_s))
            workflows[workflow['name']] = workflow
        elif line:
            part = {}
            for word in line.strip('{}\n').split(','):
                k, v = word.split('=')
                part[k] = int(v)
            parts.append(part)
    return workflows, parts


def accept_part(part, workflows):
    workflow = workflows['in']
    while True:
        for cond, target in workflow['rules']:
            if cond is None:
                result = target
            else:
                result = None
                key, op, val = cond
                if op == '<' and part[key] < val:
                    result = target
                elif op == '>' and part[key] > val:
                    result = target
            if result == 'A':
                return True
            elif result == 'R':
                return False
            elif result:
                workflow = workflows[result]
                break
            else:
                assert result is None


def add_constraint(constraints, condition):
    key, op, val = condition
    lo, hi = constraints.get(key, (1, 4000))
    if op == '>':
        if val >= hi:
            return None
        lo = val + 1
    else:
        if val <= lo:
            return None
        hi = val - 1
    return dict(constraints, **{key: (lo, hi)})


def invert(condition):
    key, op, val = condition
    return (key, '>', val - 1) if (op == '<') else (key, '<', val + 1)


def trace_paths(workflows, state):
    workflow_name, constraints = state
    for condition, target in workflows[workflow_name]['rules']:
        if condition is None:
            cons_true = constraints
        else:
            cons_true = add_constraint(constraints, condition)
            constraints = add_constraint(constraints, invert(condition))
        if cons_true is not None:
            if target == 'A':
                yield cons_true
            elif target != 'R':
                yield from trace_paths(workflows, (target, cons_true))


def count_paths(paths):
    total = 0
    for path in paths:
        total += reduce(int.__mul__, [hi - lo + 1 for lo, hi in path.values()])
    return total


def main(input_file):
    workflows, parts = parse_input(input_file)
    print("Part 1:", sum(sum(p.values()) for p in parts if accept_part(p, workflows)))
    initial_state = ('in', {r: (1, 4000) for r in 'xmas'})
    print("Part 2:", count_paths(trace_paths(workflows, initial_state)))


if __name__ == '__main__':
    main(sys.argv[1])
