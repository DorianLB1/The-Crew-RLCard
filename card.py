class CrewCard:
    info = {
        'suits': ['pink', 'yellow', 'blue', 'green'],
        'numbers': [str(num) for num in range(1, 10)],
        'rockets': ['1', '2', '3', '4']
    }

    def __init__(self, suit=None, number=None, is_rocket=False):
        ''' Initialize the class of CrewCard

        Args:
            suit (str): The suit of the card, None for Rocket cards
            number (str): The number of the card, None for Rocket cards
            is_rocket (bool): Indicator if the card is a Rocket card
        '''
        self.suit = suit
        self.number = number
        self.is_rocket = is_rocket
        self.str = self.get_str()

    def get_str(self):
        ''' Get the string representation of the card

        Return:
            (str): The string of the card's suit and number or rocket
        '''
        if self.is_rocket:
            return 'rocket-' + self.number
        else:
            return self.suit + '-' + self.number


class TaskCard:
    info = {
        'suits': ['pink', 'yellow', 'blue', 'green'],
        'number': [str(num) for num in range(1, 10)]
    }
