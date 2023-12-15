from player import Player
import random

from utils import init_crew_deck


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

    # Print initial state
    print("Initial State:")
    for i in range(num_players):
        print(f"Player {i} hand: {game.players[i].hand}")
        print(f"Player {i} task: {game.players[i].task}")

    while not game.is_round_over():
        current_player = game.game_pointer
        available_actions = game.get_available_actions(current_player)

        # Simulate a random action for the current player
        action = random.choice(available_actions)
        print(f"\nPlayer {current_player} plays action {action}")

        # Perform the action and get the new state
        new_state, next_player = game.step(action)
        print(f"New state: {new_state}")

    print("Round Over")


class TheCrewGame:
    def __init__(self, num_players):
        self.players = [Player() for _ in range(num_players)]
        self.deck, self.task_cards = init_crew_deck()
        self.shuffle_deck()
        self.deal_cards()
        self.assign_tasks()  # Placeholder for task assignment logic
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
        if len(self.current_trick) == len(self.players):
            trick_winner = determine_trick_winner(self.current_trick)
            self.players[trick_winner].won_tricks.append(self.current_trick)
            self.check_tasks_completion(trick_winner)
            self.current_trick = []
            next_player = trick_winner
        else:
            next_player = (self.game_pointer + 1) % len(self.players)
        self.game_pointer = next_player
        if self.is_round_over():
            self.update_round_end()
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
        raise ValueError("Starting player not found. Check the deck and dealing.")

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
