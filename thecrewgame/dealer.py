from thecrewgame.player import Player
import numpy as np
from thecrewgame.utils import init_crew_deck


class CrewDealer:
    ''' Initialize a Crew dealer class
    '''

    def __init__(self, np_random):
        self.np_random = np_random
        self.deck, self.task_cards_pool = init_crew_deck()
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

    def deal_task_cards(self, np_random):
        ''' Randomly select 2 task cards from the deck.
        '''
        task_cards = np_random.choice(self.task_cards_pool, 2, replace=False)
        return task_cards.tolist()

    def select_tasks(self, players, task_cards, np_random):
        ''' Each player selects a task card.
        '''
        for player in players:
            selected_card = np_random.choice(task_cards)
            player.task = selected_card
            task_cards.remove(selected_card)
            if len(task_cards) == 0:
                break




