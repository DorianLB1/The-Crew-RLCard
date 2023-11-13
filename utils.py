from card import CrewCard


def init_crew_deck():
    ''' Generate The Crew deck of 40 cards, with four suits numbered from 1 to 9
    and 4 Rocket cards.
    '''
    deck = []
    # Add numbered cards for each suit
    for suit in CrewCard.info['suits']:
        for number in CrewCard.info['numbers']:
            deck.append(CrewCard(suit=suit, number=number))

    # Add Rocket cards
    for rocket in CrewCard.info['rockets']:
        deck.append(CrewCard(number=rocket, is_rocket=True))

    return deck


if __name__ == '__main__':

    deck = init_crew_deck()
    for card in deck:
        print(card.get_str())

    cards = [CrewCard(suit='pink', number='1'), CrewCard(number='4', is_rocket=True)]

