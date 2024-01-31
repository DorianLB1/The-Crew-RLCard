class Player:
    def __init__(self):
        self.hand = []
        self.task = None
        self.communication_token = True
        self.won_tricks = []

    def show_hand(self):
        return [card.get_str() for card in self.hand]

    def show_task(self):
        if self.task:
            return self.task.get_str()
        return "No task"


def use_communication_token(player, card_index, info_type):
    ''' Player uses their communication token to reveal information about a card.

        Args:
            player (Player): The player using the token.
            card_index (int): Index of the card in player's hand to communicate about.
            info_type (str): Type of information ('highest', 'lowest', 'only').

        Returns:
            dict: Information about the card.
        '''
    if not player.communication_token:
        raise ValueError("Communication token already used.")

    card = player.hand[card_index]
    info = {'card': card.get_str(), 'info_type': info_type}
    player.communication_token = False  # Token is now used
    return info
