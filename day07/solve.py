#! /usr/bin/python3
import sys

ORDER = '*23456789TJQKA'
JACK = ORDER.index('J')
JOKER = ORDER.index('*')
HIGH_CARD, PAIR, TWO_PAIR, THREE_KIND, FULL_HOUSE, FOUR_KIND, FIVE_KIND = range(7)


def hand_type(hand):
    counts = {card: hand.count(card) for card in hand}
    assert sum(counts.values()) == 5, (hand, counts)
    if len(counts) == 5:
        assert max(counts.values()) == 1 # abcde
        return HIGH_CARD
    elif len(counts) == 4:
        assert max(counts.values()) == 2 # aabcd
        return PAIR
    elif len(counts) == 3:
        if max(counts.values()) == 2: # aabbc
            return TWO_PAIR
        assert max(counts.values()) == 3 # aaabc
        return THREE_KIND
    elif len(counts) == 2:
        if max(counts.values()) == 3: # aaabb
            return FULL_HOUSE
        assert max(counts.values()) == 4 # aaaab
        return FOUR_KIND
    elif len(counts) == 1:
        assert max(counts.values()) == 5 # aaaaa
        return FIVE_KIND
    assert 0, "unreachable"


def joker_hand_type(hand):
    n_jokers = sum(1 for card in hand if card == JOKER)
    counts = {card: hand.count(card) for card in hand}
    del counts[JOKER]
    assert sum(counts.values()) == 5 - n_jokers
    assert 1 <= n_jokers <= 5, hand
    if len(counts) == 4:
        assert n_jokers == 1 # abcdJ
        return PAIR
    elif len(counts) == 3:
        assert n_jokers in (1, 2) # aabcJ or abcJJ
        return THREE_KIND
    elif len(counts) == 2:
        assert n_jokers in (1, 2, 3) # aaabJ aabbJ aabJJ abJJJ
        if n_jokers == 1:
            if max(counts.values()) == 2:
                return FULL_HOUSE
            assert max(counts.values()) == 3
            return FOUR_KIND
        elif n_jokers == 2:
            assert max(counts.values()) == 2
            return FOUR_KIND
        assert max(counts.values()) == 1
        return FOUR_KIND
    elif len(counts) == 1:
        assert 1 <= n_jokers <= 4 # aaaaJ aaaJJ aaJJJ aJJJJ
        return FIVE_KIND
    elif len(counts) == 0:
        assert n_jokers == 5 # JJJJJ
        return FIVE_KIND
    assert 0, "unreachable"


def parse_input(path):
    hands = []
    for line in open(path).read().strip().split('\n'):
        cards, bid = line.split()
        hand = [ORDER.index(card) for card in cards]
        hands.append(((hand_type(hand), hand), int(bid)))
    return hands


def winnings(hands):
    total = 0
    for i, ((ht, hand), bid) in enumerate(sorted(hands)):
        total += (i + 1) * bid
    return total


def jokerify(hands):
    jhands = []
    for (ht, hand), bid in hands:
        if JACK in hand:
            hand = [JOKER if card == JACK else card for card in hand]
            ht = joker_hand_type(hand)
        jhands.append(((ht, hand), bid))
    return jhands


def main(input_file):
    hands = parse_input(input_file)
    print("Part 1:", winnings(hands))
    print("Part 1:", winnings(jokerify(hands)))


if __name__ == '__main__':
    main(sys.argv[1])
