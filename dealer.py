from utils import init_crew_deck
import numpy as np


class CrewDealer:
    ''' Initialize a Crew dealer class
    '''

    def __init__(self, np_random):
        self.np_random = np_random
        self.deck = init_crew_deck()
        self.shuffle()

    def shuffle(self):
        ''' Shuffle the deck
        '''
        self.np_random.shuffle(self.deck)

    def deal_cards(self, player, num):
        ''' Deal some cards from deck to one player

        Args:
            player (object): The object of a CrewPlayer
            num (int): The number of cards to be dealt
        '''
        for _ in range(num):
            if self.deck:  # Check if the deck is not empty
                player.hand.append(self.deck.pop())
            else:
                raise ValueError("The deck is empty, cannot deal more cards.")


class Player:
    def __init__(self):
        self.hand = []

    def show_hand(self):
        return [card.get_str() for card in self.hand]


if __name__ == '__main__':
    # Initialize random generator
    np_random = np.random.RandomState(42)

    # Initialize dealer
    dealer = CrewDealer(np_random)

    # Create players
    players = [Player() for _ in range(4)]

    for player in players:
        dealer.deal_cards(player, 5)

    # Show each player's hand
    for i, player in enumerate(players):
        print(f"Player {i + 1}'s hand: {player.show_hand()}")