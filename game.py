import numpy as np

from card import CrewCard
from dealer import CrewDealer
from player import Player
from utils import find_commander, check_task_completion
from player import use_communication_token


def play_a_trick(players, current_player_index):
    first_suit = None
    winning_card = None
    winning_player_index = current_player_index
    rocket_played = False
    trick_cards = []

    for i in range(len(players)):
        player_index = (current_player_index + i) % len(players)
        player = players[player_index]

        # Player plays the first card in their hand
        card = player.hand.pop(0)
        trick_cards.append(card)
        print(f"Player {player_index + 1} plays {card.get_str()}")

        if card.is_rocket:  # Check if the card is a rocket
            if not rocket_played or int(card.number) > int(winning_card.number):
                winning_card = card
                winning_player_index = player_index
                rocket_played = True
        elif not rocket_played:
            if first_suit is None:
                first_suit = card.suit
                winning_card = card
                winning_player_index = player_index
            elif card.suit == first_suit and int(card.number) > int(winning_card.number):
                winning_card = card
                winning_player_index = player_index

    # Add the entire trick to the winner's won tricks
    players[winning_player_index].won_tricks.append(trick_cards)

    return winning_card, winning_player_index, trick_cards


def all_tasks_completed(players):
    for player in players:
        if player.task:  # Consider only players with tasks
            # Task is completed if the player's task card matches a winning card
            if not check_task_completion(player, player.task):
                print(f"Player {players.index(player) + 1} task not completed: {player.task.get_str()}")  # Debug
                return False  # If any task is not completed, return False
    return True  # Return True if all tasks are completed


def is_game_over(players):
    all_cards_played = all(len(player.hand) == 0 for player in players)
    all_tasks_done = all_tasks_completed(players)

    print(f"Debug: All cards played: {all_cards_played}, All tasks done: {all_tasks_done}")  # Debugging line

    return all_cards_played or all_tasks_done


def play_game(players, commander_index):
    current_player_index = commander_index
    trick_number = 1

    while True:  # Continue until the game is over
        print(f"\n--- Trick {trick_number} ---")
        print(f"Player {current_player_index + 1} starts the trick.")

        # Players play a trick
        winning_card, winner_index, trick_cards = play_a_trick(players, current_player_index)
        print(f"Player {winner_index + 1} wins the trick with {winning_card.get_str()}")

        # Add the winning card to the winner's list of won tricks
        players[winner_index].won_tricks.append(trick_cards)

        # Check task completion if the player has a task
        if players[winner_index].task:
            task_card = players[winner_index].task
            task_completed = check_task_completion(players[winner_index], task_card)
            if task_completed:
                print(f"Player {winner_index + 1} completes their task with {winning_card.get_str()}!")
                players[winner_index].task = None  # Mark the task as completed
            else:
                print(f"Player {winner_index + 1} did not complete a task.")
        else:
            print(f"Player {winner_index + 1} wins the trick but has no task.")

        # Increment trick number
        trick_number += 1

        # Check if the game should end
        if is_game_over(players):
            break

    # Determine if the mission is successful
    if all_tasks_completed(players):
        print("Mission successful!")
    else:
        print("Mission failed.")


if __name__ == '__main__':
    # Initialize random generator
    np_random = np.random.RandomState()

    # Initialize dealer
    dealer = CrewDealer(np_random)

    # Create players
    players = [Player() for _ in range(4)]

    # Deal cards to players
    for player in players:
        dealer.deal_cards(player, 10)

    # Shuffle task cards pool and select tasks
    np_random.shuffle(dealer.task_cards_pool)
    task_cards = dealer.deal_task_cards(np_random)
    dealer.select_tasks(players, task_cards, np_random)

    # Show each player's hand and their tasks
    for i, player in enumerate(players):
        print(f"Player {i + 1}'s hand: {player.show_hand()}")
        print(f"Player {i + 1}'s task: {player.show_task()}")

    # Find the starting player (Commander)
    commander_index = find_commander(players)
    print(f"Player {commander_index + 1} is the Commander")

    # Play the game
    play_game(players, commander_index)
