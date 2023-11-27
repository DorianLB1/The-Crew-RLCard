import numpy as np

from card import CrewCard
from dealer import CrewDealer
from player import Player
from utils import find_commander
from player import use_communication_token


def play_a_trick(players, current_player_index):
    first_suit = None
    winning_card = None
    winning_player_index = current_player_index

    for i in range(len(players)):
        # Determine which player is playing
        player_index = (current_player_index + i) % len(players)
        player = players[player_index]

        # Player plays the first card in their hand (or implement a strategy)
        card = player.hand.pop(0)
        print(f"Player {player_index + 1} plays {card.get_str()}")

        # Determine the winning card
        if first_suit is None:
            first_suit = card.suit
            winning_card = card
            winning_player_index = player_index
        elif card.suit == first_suit and int(card.number) > int(winning_card.number):
            winning_card = card
            winning_player_index = player_index

    return winning_card, winning_player_index



def find_winner_and_check_task(players, winning_card):
    ''' Find the winner of the trick and check if their task is completed.

    Args:
        players (list): List of Player objects
        winning_card (CrewCard): The card that won the trick
    '''
    for player in players:
        if player.task and player.task.get_str() == winning_card.get_str():
            print(
                f"Player {players.index(player) + 1} wins the trick with {winning_card.get_str()} and completes the task!")
            return True
    return False


if __name__ == '__main__':
    np_random = np.random.RandomState()

    # Initialize dealer
    dealer = CrewDealer(np_random)

    # Create players
    players = [Player() for _ in range(4)]

    for player in players:
        dealer.deal_cards(player, 10)

    task_cards = dealer.deal_task_cards(np_random)
    dealer.select_tasks(players, task_cards, np_random)

    # Show each player's hand
    for i, player in enumerate(players):
        print(f"Player {i + 1}'s hand: {player.show_hand()}")
        print(f"Player {i + 1}'s task: {player.show_task()}")

    starting_player_index = find_commander(players)
    print(f"Player {starting_player_index + 1} is the Commander")

    # Example of a player using the communication token
    if players[0].communication_token:
        info = use_communication_token(players[0], 0, 'highest')
        print(f"Player 1 communicates: {info}")

    # Simulate playing a trick
    winning_card = play_a_trick(players)
    task_completed = find_winner_and_check_task(players, winning_card)
    print(f"Task completed: {task_completed}")

