from card import CrewCard


def init_crew_deck():
    ''' Generate The Crew deck of 40 cards, with four suits numbered from 1 to 9
    and 4 Rocket cards. Also, prepare a set of potential Task Cards.
    '''
    deck = []
    task_cards = []
    # Add numbered cards for each suit
    for suit in CrewCard.info['suits']:
        for number in CrewCard.info['numbers']:
            card = CrewCard(suit=suit, number=number)
            deck.append(card)
            task_cards.append(card)

    # Add Rocket cards
    for rocket in CrewCard.info['rockets']:
        card = CrewCard(number=rocket, is_rocket=True)
        deck.append(card)

    return deck, task_cards


def find_commander(players):
    ''' Finds the starting player (the one who has the "Rocket 4" card)

    Args:
        players (list): The list of Player objects

    Returns:
        int: The index of the starting player
    '''
    for i, player in enumerate(players):
        for card in player.hand:
            if card.get_str() == 'rocket-4':
                return i
    raise ValueError("Rocket 4 card not found. Check the deck and dealing.")


def check_task_completion(player, winning_card):
    ''' Check if the player has completed their task.

    Args:
        player (Player): The player object
        winning_card (CrewCard): The card that won the trick

    Returns:
        bool: True if the task is completed, False otherwise
    '''
    if player.task.get_str() == winning_card.get_str():
        return True
    return False


if __name__ == '__main__':

    deck = init_crew_deck()
    for card in deck:
        print(card.get_str())

    cards = [CrewCard(suit='pink', number='1'), CrewCard(number='4', is_rocket=True)]
