from collections import Counter


def data(filepath):
    with open(filepath, "r") as f:
        lines = f.read().splitlines()

    hands = list()
    for line in lines:
        dirty_line = line.split()
        hand = dirty_line[0]
        bid = int(dirty_line[1])
        hands.append((hand, bid))

    return hands


class Hand():
    def __init__(self, hand, order):
        self.hand = list(hand[0])
        self.order = order
        self.bid = hand[1]
        self.type_order = [
            self.is_five,
            self.is_four,
            self.is_full_house,
            self.is_three,
            self.is_two_pair,
            self.is_pair,
            self.is_high_card
        ]
        self.type = self._type()
        self.sort_score = [self.order.index(card) for card in self.hand]
        self.sort()

    @property
    def count(self):
        return Counter(self.hand)

    def __str__(self):
        return f"{str(self.hand)}: {self.bid}"

    def __repr__(self):
        return f"{str(self.hand)}: {self.bid}"

    def _type(self):
        for score, func in enumerate(self.type_order):
            if func():
                return score

    def _custom_sort(self, element):
        return self.order.index(element)

    def sort(self):
        self.hand.sort(key=self._custom_sort)

    def is_five(self):
        return len(set(self.hand)) == 1

    def is_four(self):
        return 4 in self.count.values()

    def is_full_house(self):
        return 3 in self.count.values() and 2 in self.count.values()

    def is_three(self):
        return 3 in self.count.values()

    def is_two_pair(self):
        return 2 == list(self.count.values()).count(2)

    def is_pair(self):
        return 1 == list(self.count.values()).count(2)

    def is_high_card(self):
        return True


class HandTwo(Hand):
    def __init__(self, hand, order):
        super().__init__(hand, order)
        self.jokers = self.hand.count("J")
        if self.jokers:
            self.type = self._wild_types()
        else:
            self.type = self._type()

    def __repr__(self):
        return f"{str(self.hand)}: {self.type}: {self.bid}"

    def _wild_types(self):
        c_types = set(self.hand)
        tmp_hand = self.hand

        types = list()
        for card in c_types:
            self.hand = list(map(lambda x: x.replace('J', card), self.hand))
            types.append(self._type())
            self.hand = tmp_hand

        return min(types)


if __name__ == "__main__":
    hand_data = data("input.txt")

    hands = list()
    order = [
        "A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"
    ]
    for hand in hand_data:
        hands.append(Hand(hand, order))

    result = sorted(hands, key=lambda hand: (hand.type, hand.sort_score))

    answer = 0
    for index, hand in enumerate(reversed(result)):
        rank = index + 1
        answer += rank * hand.bid

    print(f"Answer 1: {answer}")

    # Puzzle 2
    hands = list()
    order = [
        "A", "K", "Q", "T", "9", "8", "7", "6", "5", "4", "3", "2", "J"
    ]
    for hand in hand_data:
        hands.append(HandTwo(hand, order))

    result = sorted(hands, key=lambda hand: (hand.type, hand.sort_score))
    answer = 0
    for index, hand in enumerate(reversed(result)):
        rank = index + 1
        answer += rank * hand.bid

    print(f"Answer 2: {answer}")
