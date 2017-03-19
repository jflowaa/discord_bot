import random

import settings


class GuessingGame:
    """Guessing game plugin"""

    def __init__(self):
        self.guessing_game_active = False
        self.guesses = {}
        self.answer = 0
        self.game_channel = None
        self.local_random = random.Random()

    def is_game_active(self):
        """Is the game active."""
        return self.guessing_game_active

    def generate_answer(self):
        """Get a random number from the given range."""
        self.answer = self.local_random.randint(1, settings.GUESSING_GAME_MAX)

    def start_game(self, channel):
        """Starts the game for the channel."""
        self.guessing_game_active = True
        self.game_channel = channel
        self.generate_answer()

    def end_game(self):
        """Ends the game."""
        self.guessing_game_active = False

    def add_guess(self, message):
        """Someone guessed, add it to the pool"""
        self.guesses[message.author] = message.content

    def check_for_winner(self):
        """Check for winner, could be multiple winners"""
        winner_list = []
        for key, value in self.guesses.items():
            if int(value) == self.answer:
                winner_list.append(key)
        if winner_list:
            return self.create_winner_message(winner_list)
        else:
            return "No one guessed the correct answer of: **{}**".format(self.answer)

    @staticmethod
    def create_winner_message(winner_list):
        """Message used when declaring a winner"""
        if len(winner_list) > 1:
            return "The winners are: " + ",".join(winner_list)
        else:
            return "The winner is: {}".format(winner_list[0])

    def get_starting_message(self):
        return """Guessing game started!
Say a number in chat between 1 and {}
The game will end in {} seconds""".format(settings.GUESSING_GAME_MAX, settings.GUESSING_GAME_LENGTH)
