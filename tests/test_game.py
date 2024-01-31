import unittest
from thecrewgame.game import TheCrewGame


class TestTheCrewGame(unittest.TestCase):

    def setUp(self):
        self.game = TheCrewGame(num_players=4)

    def test_initialization(self):
        self.assertEqual(len(self.game.players), 4)

    def test_play_card(self):
        self.game.game_pointer = 0
        initial_hand_size = len(self.game.players[0].hand)
        self.game.step(0)
        self.assertEqual(len(self.game.players[0].hand), initial_hand_size - 1, "Hand size did not decrease")
        self.assertEqual(len(self.game.current_trick), 1, "Current trick size is not 1")


if __name__ == '__main__':
    unittest.main()
