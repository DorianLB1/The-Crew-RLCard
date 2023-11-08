class CrewCard:
    info = {
        'suits': ['pink', 'yellow', 'blue', 'green'],
        'number': [str(num) for num in range(1, 10)],
        'rocket': ['1', '2', '3', '4']
    }

    def __init__(self, suits, number, is_rocket=False):
        """
        Initialize the CrewCard Class


        Args :
            suits(str) : The color of the card
            number (str) : The number of the card (1 to 9)
            is_rocket (boolean) : Indicator if the card is a Rocket
        """

        self.suits = suits
        self.number = number
        self.is_rocket = is_rocket
        self.str = self.getstr()

    def getstr(self):
        """
        Get the string representation of the card

        :return:
            (str): The string of the card's suits (color) and number or if it's a rocket
        """
        if self.is_rocket:
            return 'rocket-' + self.number
        else:
            return self.suits + self.number


class TaskCard:
    info = {
        'suits': ['pink', 'yellow', 'blue', 'green'],
        'number': [str(num) for num in range(1, 10)]
    }
