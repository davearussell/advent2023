#! /usr/bin/python3
import copy
import itertools
import math
import sys


def parse_input(path):
    modules = {}
    for line in open(path).read().strip().replace('broadcaster', 'bbroadcaster').split('\n'):
        label, outputs = line.split(' -> ')
        prefix, mname = label[0], label[1:]
        mtype = 'flip' if prefix == '%' else 'conj' if prefix == '&' else 'bcast'
        module = modules.setdefault(mname, {'name': mname, 'inputs': [], 'outputs': []})
        module['mtype'] = mtype
        for output in outputs.split(', '):
            module['outputs'].append(output)
            output_module = modules.setdefault(output, {'name': output, 'inputs': [], 'outputs': []})
            output_module['inputs'].append(mname)
    return modules


def press_button(modules):
    signals = [('button', 'broadcaster', 0)]
    while signals:
        new_signals = []
        for src, dst, lvl in signals:
            yield dst, lvl
            out_lvl = None
            module = modules[dst]
            if module.get('mtype') == 'bcast':
                out_lvl = lvl
            elif module.get('mtype') == 'flip':
                if not lvl:
                    out_lvl = module['state'] = 1 - module.get('state', 0)
            elif module.get('mtype') == 'conj':
                n_inputs = len(module['inputs'])
                state = module.setdefault('state', [0 for _ in module['inputs']])
                state[module['inputs'].index(src)] = lvl
                out_lvl = 0 if state.count(1) == n_inputs else 1
            if out_lvl is not None:
                for out in module['outputs']:
                    new_signals.append((dst, out, out_lvl))
        signals = new_signals


def count_pulses(modules, button_presses):
    counts = [0, 0]
    for i in range(button_presses):
        for _, lvl in press_button(modules):
            counts[lvl] += 1
    return math.prod(counts)


def reachable_from(module, modules):
    names = set()
    todo = [module['name']]
    while todo:
        name = todo.pop()
        if name not in names:
            names.add(name)
            todo += modules[name].get('outputs', [])
    return names


def partition_modules(modules):
    for mname in modules['broadcaster']['outputs']:
        partition = copy.deepcopy(modules)
        to_keep = reachable_from(modules[mname], modules) | {'broadcaster'}
        for name in list(partition):
            if name not in to_keep:
                module = partition.pop(name)
                for dst_name in module['outputs']:
                    partition[dst_name]['inputs'].remove(name)
                for src_name in module['inputs']:
                    partition[src_name]['outputs'].remove(name)
        yield partition


def time_to_rx_low(modules):
    for n in itertools.count(1):
        if ('rx', 0) in press_button(modules):
            return n


def main(input_file):
    modules = parse_input(input_file)
    print("Part 1:", count_pulses(copy.deepcopy(modules), 1000))

    # For part 2 I make these assumptions that are true for at least my input:
    # 1. The module graph diverges after leaving the broadcaster and only converges
    #    again into a single CONJ that then feeds into RX
    # 2. Each section of the feeds a 0 into RX on the same button press that its state resets
    # 3. Each section always feeds a 0 into RX at the same time within the cycle
    #
    # Given the above I can model each section of the graph separately to determine when it
    # drives RX low. RX will go low in the full graph at the LCM of the per-section counts.
    cycle_lengths = [time_to_rx_low(partition) for partition in partition_modules(modules)]
    print("Part 2:", math.lcm(*cycle_lengths))


if __name__ == '__main__':
    main(sys.argv[1])
