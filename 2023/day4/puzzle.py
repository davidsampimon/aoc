import re
import heapq
import time


def data(filepath):
    with open(filepath, "r") as f:
        lines = f.read().splitlines()

    data = {}
    for line in lines:
        dirty_data = line.split(":")
        card_num = int(re.findall(r"\d+", dirty_data.pop(0))[0])
        dirty_nums = dirty_data.pop(0)
        dirty_winners, dirty_card_nums = dirty_nums.split("|")
        winners = [int(x) for x in re.findall(r"\d+", dirty_winners)]
        card_nums = [int(x) for x in re.findall(r"\d+", dirty_card_nums)]
        data[card_num] = {
            "winners": winners,
            "nums": card_nums,
            "score": 0,
            "copies": list()
        }
    return data


class CardDeck():
    def __init__(self, cards):
        self.cards = cards
        self.heap = list(cards)
        heapq.heapify(self.heap)
        self.total_cards = 0


    def play_game(self):
        while self.heap:
            card = heapq.heappop(self.heap)
            self.total_cards += 1
            for copy in self.cards[card]["copies"]:
                heapq.heappush(self.heap, copy)

        return self.total_cards


if __name__ == "__main__":
    cards = data("input.txt")

    # Puzzle 1
    answer = 0
    for game, card in cards.items():
        hits = 0
        for num in card["nums"]:
            if num in card["winners"]:
                hits += 1

        cards[game]["score"] = pow(2, hits-1) if hits > 0 else 0
        cards[game]["copies"] = [game + hit for hit in range(1, hits + 1)]

    for game, card in cards.items():
        answer += card["score"]
    print(f"Answer 1: {answer}")

    # Puzzle 2
    cd = CardDeck(cards)
    start = time.perf_counter()
    total_cards = cd.play_game()
    stop = time.perf_counter()
    print(f"Answer 2: {total_cards}")
    print(f"In {stop - start} seconds!")
