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



if __name__ == '__main__':

    deck = init_crew_deck()
    for card in deck:
        print(card.get_str())

    cards = [CrewCard(suit='pink', number='1'), CrewCard(number='4', is_rocket=True)]
