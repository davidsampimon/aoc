import unittest

from day23.puzzle import Game, Blueprint, Inventory, parse_input


class TestInventory(unittest.TestCase):
    def setUp(self):
        self.blueprints = parse_input("test.txt")
        self.inventory = Inventory()

    def test_creation(self):
        blueprint = self.blueprints[0]
        results = []
        for robot_func in blueprint.price_card.keys():
            results.append(self.inventory.materials[robot_func] == 0)
        assert all(results)

    def test_play_round_geode_bot(self):
        self.inventory.add_robot("geode")
        self.inventory.play_round()
        assert self.inventory.materials["geode"] == 1

    def test_play_rounds_ore_bot(self):
        rounds = 5
        self.inventory.add_robot("ore")
        for _ in range(rounds):
            self.inventory.play_round()
        assert self.inventory.materials["ore"] == rounds
        assert self.inventory.materials["obsidian"] == 0
        assert self.inventory.materials["clay"] == 0
        assert self.inventory.materials["geode"] == 0

    def test_play_rounds_obsidian_bot(self):
        rounds = 5
        self.inventory.add_robot("obsidian")
        for _ in range(rounds):
            self.inventory.play_round()
        assert self.inventory.materials["obsidian"] == rounds
        assert self.inventory.materials["ore"] == 0
        assert self.inventory.materials["clay"] == 0
        assert self.inventory.materials["geode"] == 0

    def test_play_rounds_clay_bot(self):
        rounds = 5
        self.inventory.add_robot("clay")
        for _ in range(rounds):
            self.inventory.play_round()
        assert self.inventory.materials["clay"] == rounds
        assert self.inventory.materials["obsidian"] == 0
        assert self.inventory.materials["ore"] == 0
        assert self.inventory.materials["geode"] == 0

    def test_play_rounds_geode_bot(self):
        rounds = 5
        self.inventory.add_robot("geode")
        for _ in range(rounds):
            self.inventory.play_round()
        assert self.inventory.materials["geode"] == rounds
        assert self.inventory.materials["ore"] == 0
        assert self.inventory.materials["obsidian"] == 0
        assert self.inventory.materials["clay"] == 0

class TestGame(unittest.TestCase):
    def setUp(self):
        blueprints = parse_input("test.txt")
        self.game = Game(blueprints[0])

    def test_play_round(self):
        inventory = Inventory()
        inventory.add_robot("geode")
        geode_result = self.game.play_round(inventory, 2)
        assert geode_result == 2
    
    def test_play_rounds(self):
        inventory = Inventory()
        inventory.add_robot("geode")
        geode_result = self.game.play_round(inventory, 10)
        assert geode_result == 10
    
    def test_play_ore_bot(self):
        inventory = Inventory()
        inventory.add_robot("ore")
        inventory.add_robot("geode")
        geode_result = self.game.play_round(inventory, 4)
        assert geode_result == 4

    def test_pay_robot(self):
        inventory = Inventory()
        inventory = self.game.pay_robot(inventory, "geode")
        assert inventory.materials["ore"] == -2
        assert inventory.materials["obsidian"] == -7
        assert inventory.materials["clay"] == 0
        assert inventory.materials["geode"] == 0
        

    def test_options(self):
        inventory = Inventory()
        for _ in range(14):
            inventory.add_material("ore")
            inventory.add_material("clay")
        options = self.game.options(inventory)
        assert options == [
            "Do nothing",
            "ore",
            "clay",
            "obsidian",
        ]

    def test_options_nothing(self):
        inventory = Inventory()
        options = self.game.options(inventory)
        assert options == [
            "Do nothing"
        ]
    
    def test_options_only_return_geode(self):
        inventory = Inventory()
        for _ in range(10):
            inventory.add_material("ore")
            inventory.add_material("obsidian")
        options = self.game.options(inventory)
        assert options == [
            "geode",
        ]

    def test_play_round_with_buy(self):
        inventory = Inventory()
        for _ in range(10):
            inventory.add_material("ore")
            inventory.add_material("obsidian")
        geode_result = self.game.play_round(inventory, 4)
        assert geode_result == 3
    

if __name__ == '__main__':
    unittest.main()