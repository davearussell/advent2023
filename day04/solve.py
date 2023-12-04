#! /usr/bin/python3
import sys


def parse_input(path):
    cards = []
    for line in open(path):
        words = line.split()[2:] # drop 'Card #:'
        sep = words.index('|')
        win = {int(word) for word in words[:sep]}
        have = {int(word) for word in words[sep+1:]}
        cards.append(len(win & have)) # we only need the number of matches
    return cards


def score(card):
    return 1 << (card - 1) if card else 0


def enumerate_copies(cards):
    counts = [1 for _ in cards]
    for i, card in enumerate(cards):
        for j in range(card):
            if i + j + 1 < len(counts):
                counts[i + j + 1] += counts[i]
    return counts


def main(input_file):
    cards = parse_input(input_file)
    print("Part 1:", sum(map(score, cards)))
    print("Part 2:", sum(enumerate_copies(cards)))


if __name__ == '__main__':
    main(sys.argv[1])
