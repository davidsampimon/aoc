import unittest

from day23.puzzle import parse_input
from paste import GameState, choose_paths


class TestOptions(unittest.TestCase):
    def setUp(self):
        blueprints = parse_input("test.txt")
        self.game = GameState(blueprints[0].price_card, 1)
        self.game.add_robot("ore")

    def test_options(self):
        options = choose_paths(self.game)
        assert options == ["Do nothing"]

    def test_options_geode(self):
        costs = self.game.price_card["geode"]
        for cost in costs:
            self.game.add_material(cost[0], cost[1])
        options = choose_paths(self.game)
        assert options == ["geode"]

    def test_exclude_bot(self):
        for bot, amount in self.game.max_spend.items():
            for _ in range(amount):
                self.game.add_robot(bot)

        for bot_costs in self.game.price_card.values():
            for cost in bot_costs:
                self.game.add_material(cost[0], cost[1] * 3 )
        options = choose_paths(self.game)
        assert options == ["geode"]



if __name__ == '__main__':
    unittest.main()