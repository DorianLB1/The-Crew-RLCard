from thecrewgame.player import Player
import random

from thecrewgame.utils import init_crew_deck


def encode_task(task):
    return task.get_str() if task else None


def encode_trick(trick):
    return [card.get_str() for card in trick]


def encode_cards(cards):
    return [card.get_str() for card in cards]


def determine_trick_winner(trick):
    leading_suit = trick[0].suit
    winning_card = trick[0]
    winner_index = 0

    for i, card in enumerate(trick[1:], 1):
        if card.is_rocket:
            if not winning_card.is_rocket or int(card.number) > int(winning_card.number):
                winning_card = card
                winner_index = i
        elif not winning_card.is_rocket and card.suit == leading_suit and int(card.number) > int(
                winning_card.number):
            winning_card = card
            winner_index = i

    return winner_index


def check_task_completion(player, task_card):
    ''' Check if the player has completed their task.
    Args:
        player (Player): The player object
        task_card (CrewCard): The card object representing the player's task
    Returns:
        bool: True if the task is completed, False otherwise
    '''
    for trick in player.won_tricks:
        if task_card in trick:
            return True
    return False


def simulate_game():
    num_players = 4
    game = TheCrewGame(num_players)

    print("Initial State:")
    for i in range(num_players):
        player_hand = ', '.join([card.get_str() for card in game.players[i].hand])
        task = game.players[i].task.get_str() if game.players[i].task else "No task"
        print(f"Player {i} hand: {player_hand}")
        print(f"Player {i} task: {task}")

    print("\n--- Game Start ---\n")
    round_number = 1

    while not game.is_round_over():
        if len(game.current_trick) == 0:
            print(f"\n--- Round {round_number} ---\n")
            round_number += 1

        current_player = game.game_pointer
        available_actions = game.get_available_actions(current_player)
        action = random.choice(available_actions)
        played_card = game.players[current_player].hand[action].get_str()
        print(f"Player {current_player} plays {played_card}")

        new_state, next_player = game.step(action)

        # Display current trick after each player's action, but before it's cleared
        current_trick = ', '.join(new_state['public_info']['current_trick'])
        print(f"Current trick: {current_trick}\n")

        if game.is_round_over():
            print("Round Over")
            break

    print("\nTask Completion Status:")
    for i in range(num_players):
        task_status = "Completed" if game.players[i].task is None else "Not Completed"
        print(f"Player {i} task: {task_status}")


class TheCrewGame:
    def __init__(self, num_players):
        self.current_trick_pending_clear = False
        self.players = [Player() for _ in range(num_players)]
        self.deck, self.task_cards = init_crew_deck()
        self.shuffle_deck()
        self.deal_cards()
        self.commander_index = self.find_commander()
        self.assign_tasks()
        self.current_trick = []
        self.game_pointer = self.find_commander()

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def deal_cards(self):
        for player in self.players:
            for _ in range(10):  # Assuming each player gets 10 cards
                player.hand.append(self.deck.pop())

    def assign_tasks(self):
        random.shuffle(self.task_cards)
        self.players[0].task = self.task_cards.pop()
        self.players[1].task = self.task_cards.pop()

    def get_state(self, player_id):
        state = {}
        state['actions'] = self.get_available_actions(player_id)
        state['player_hand'] = encode_cards(self.players[player_id].hand)
        state['current_trick'] = encode_trick(self.current_trick)
        state['player_task'] = encode_task(self.players[player_id].task)
        state['public_info'] = self.get_public_info()
        for i in range(len(self.players)):
            if i != player_id:
                state['player' + str(i) + '_num_cards'] = len(self.players[i].hand)
        return state

    def get_available_actions(self, player_id):
        player_hand = self.players[player_id].hand
        return list(range(len(player_hand)))

    def step(self, action):
        if action not in self.get_available_actions(self.game_pointer):
            raise ValueError("Invalid action.")

        played_card = self.players[self.game_pointer].hand.pop(action)
        self.current_trick.append(played_card)

        next_player = (self.game_pointer + 1) % len(self.players)

        if len(self.current_trick) == len(self.players):
            trick_winner = determine_trick_winner(self.current_trick)
            self.players[trick_winner].won_tricks.append(list(self.current_trick))

            self.check_tasks_completion(trick_winner)

            next_player = trick_winner
            self.current_trick.clear()

            if self.is_round_over():
                self.update_round_end()

        self.game_pointer = next_player

        return self.get_state(self.game_pointer), self.game_pointer

    def get_public_info(self):
        public_info = {}
        for i, player in enumerate(self.players):
            public_info['player{}_num_cards'.format(i)] = len(player.hand)
        public_info['current_trick'] = [card.get_str() for card in self.current_trick]
        return public_info

    def check_tasks_completion(self, player_id):
        player = self.players[player_id]
        if player.task:
            task_completed = check_task_completion(player, player.task)
            if task_completed:
                player.task = None

    def find_commander(self):
        for i, player in enumerate(self.players):
            for card in player.hand:
                if card.get_str() == 'rocket-4':
                    return i
        return None

    def is_round_over(self):
        all_cards_played = all(len(player.hand) == 0 for player in self.players)
        all_tasks_completed = all(
            player.task is None or check_task_completion(player, player.task) for player in self.players if
            player.task is not None)
        return all_cards_played or all_tasks_completed

    def update_round_end(self):
        pass


if __name__ == "__main__":
    simulate_game()
