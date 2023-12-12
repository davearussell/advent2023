#! /usr/bin/python3
import sys
import time


def parse_input(path):
    rows = []
    for line in open(path):
        springs, _counts = line.split()
        counts = tuple(int(count) for count in _counts.split(','))
        rows.append((springs, counts))
    return rows


def count_regions(springs):
    l = []
    n = 0
    for i, spring in enumerate(springs):
        if spring == '?':
            if n:
                l.append(-n) # negative value indicates an in-progress count that may grow
            return tuple(l)
        elif spring == '#':
            n += 1
        elif n:
            l.append(n)
            n = 0
    if n:
        l.append(n)
    return tuple(l)


CACHE = {}
def count_ways(springs, counts, verbose=False, skipped=''):
    def log(msg):
        if verbose:
            print ("count_ways \x1b[31m%s\x1b[0m%s %r %s" % (skipped, springs, counts, msg))
        
    so_far = count_regions(springs)

    qi = springs.find('?')
    if qi == -1:
        result = 1 if so_far == counts else 0
        log("VALID" if result else "INVALID")
        return result

    di = springs[:qi].rfind('.')
    if di != -1:
        qi -= (di + 1)
        skipped += springs[:di + 1]
        springs = springs[di + 1:]
        if so_far:
            done_counts = len(so_far)
            if done_counts and so_far[-1] < 0: # in-progress counts can't be considered done
                done_counts -= 1
            if so_far[:done_counts] != counts[:done_counts]:
                log("bad done_counts %r %r" % (so_far, counts))
                return 0
            so_far = so_far[done_counts:]
            counts = counts[done_counts:]
            if so_far and (not counts or -so_far[0] > counts[0]):
                log("bad in-progress count")
                return 0

    cached = CACHE.get((springs, counts))
    if cached is not None:
        log("return cached %r" % (cached,))
        return cached

    gsprings = '%s.%s' % (springs[:qi], springs[qi+1:])
    bsprings = '%s#%s' % (springs[:qi], springs[qi+1:])
    log('recurse')
    result = (count_ways(gsprings, counts, verbose, skipped) +
              count_ways(bsprings, counts, verbose, skipped))
    CACHE[(springs, counts)] = result
    return result


def sum_rows(rows, verbose):
    total = 0
    for i, row in enumerate(rows):
        t0 = time.time()
        n = count_ways(*row, verbose=verbose > 1)
        total += n
        if verbose:
            print("row %d: %d in %.2fs" % (i, n, time.time() - t0))
    return total


def unfold(rows):
    new_rows = []
    for springs, counts in rows:
        new_rows.append(('?'.join([springs] * 5), counts * 5))
    return new_rows


def main(input_file):
    rows = parse_input(input_file)
    big_rows = unfold(rows)
    # 0: no logging
    # 1: log time to solve each row
    # 2: log every permutation
    verbose = 0
    print("Part 1:", sum_rows(rows, verbose))
    print("Part 2:", sum_rows(big_rows, verbose))


if __name__ == '__main__':
    main(sys.argv[1])
