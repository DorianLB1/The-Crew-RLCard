import unittest
from thecrewgame.card import CrewCard


class TestCrewCard(unittest.TestCase):

    def test_rocket_card_creation(self):
        card = CrewCard(is_rocket=True, number='4')
        self.assertEqual(card.get_str(), 'rocket-4')

    def test_regular_card_creation(self):
        card = CrewCard(suit='pink', number='3')
        self.assertEqual(card.get_str(), 'pink-3')

    def test_invalid_card(self):
        with self.assertRaises(ValueError):
            CrewCard(suit='invalid', number='10')


if __name__ == '__main__':
    unittest.main()