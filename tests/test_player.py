import unittest
from thecrewgame.player import Player
from thecrewgame.card import CrewCard


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player()
        self.card = CrewCard(suit='pink', number='5')

    def test_add_card_to_hand(self):
        self.player.hand.append(self.card)
        self.assertIn(self.card, self.player.hand)

    def test_remove_card_from_hand(self):
        self.player.hand.append(self.card)
        self.player.hand.remove(self.card)
        self.assertNotIn(self.card, self.player.hand)

    def test_set_task(self):
        task = CrewCard(suit='blue', number='3')
        self.player.task = task
        self.assertEqual(self.player.task, task)


if __name__ == '__main__':
    unittest.main()
