import unittest
from thecrewgame.dealer import CrewDealer
from numpy.random import RandomState
from thecrewgame.player import Player


class TestCrewDealer(unittest.TestCase):

    def setUp(self):
        self.np_random = RandomState()
        self.dealer = CrewDealer(self.np_random)

    def test_deck_shuffle(self):
        deck_before_shuffle = self.dealer.deck[:]
        self.dealer.shuffle()
        deck_after_shuffle = self.dealer.deck
        self.assertNotEqual(deck_before_shuffle, deck_after_shuffle)

    def test_deal_cards(self):
        player = Player()
        self.dealer.deal_cards(player, 5)
        self.assertEqual(len(player.hand), 5)

    def test_deal_task_cards(self):
        task_cards = self.dealer.deal_task_cards(self.np_random)
        self.assertEqual(len(task_cards), 2)


if __name__ == '__main__':
    unittest.main()
