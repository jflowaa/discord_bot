import random
import sqlite3
import operator
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


class BotLogic:

    def __init__(self):
        self.guessing_game_active = False
        self.guesses = {}
        self.answer = 0
        self.game_channel = None
        self.local_random = random.Random()
        self.create_db()
        self.bad_chars = [".", "?", "!", " ", ","]

    def create_db(self):
        self.connection = sqlite3.connect("word_count.db")
        self.connection.execute(
            """
                create table if not exists words
                (id integer primary key autoincrement,
                author char(75) not null,
                word char(75) not null,
                count int not null);
            """)

    def track_word_count(self, message):
        author = message.author.display_name
        words = message.content.split()
        for word in words:
            word = "".join([c for c in word if c not in self.bad_chars]).lower()
            if len(word) > 2:
                data = self.connection.execute("select id, count from words where word=? and author=?", (word, author)).fetchone()
                if data:
                    self.connection.execute("update words set count=? where id=?", (data[1]  + 1, data[0]))
                else:
                    self.connection.execute("insert into words (author, word, count) values (?, ?, ?)", (author, word, 1))
                self.connection.commit()

    def get_word_stats(self, author=None):
        if author:
            data = self.connection.execute("select word, count from words where author=?", (str(author),)).fetchall()
        else:
            data = self.connection.execute("select word, count from words").fetchall()
        stats = {}
        for d in data:
            stats[d[0]] = d[1]
        sorted_stats = sorted(stats.items(), key=operator.itemgetter(1), reverse=True)
        return self.chart_stats(sorted_stats)

    def get_stats_for_word(self, word):
        data = self.connection.execute("select word, count from words where word=?", (word,)).fetchone()
        if data:
            count = data[1]
        else:
            count = 0
        data = "The word '{}' has been used: **{}**".format(word, count)
        return data

    def chart_stats(self, stats):
        word_list, count_list = zip(*stats[:25])
        plt.barh(range(len(word_list)), count_list, align="center", height=0.5)
        plt.yticks(range(len(word_list)), word_list)
        plt.xlabel("Number of Times")
        plt.xticks(range(max(count_list) + 1))
        plt.savefig("chart.png")
        return "chart.png"

    def db_wipe(self):
        self.connection.execute("drop table if exists words")
        self.connection.execute(
            """
                create table if not exists words
                (id integer primary key autoincrement,
                author char(75) not null,
                word char(75) not null,
                count int not null);
            """)

    def is_game_active(self):
        return self.guessing_game_active

    def generate_answer(self):
        self.answer = self.local_random.randint(1, 10)

    def start_game(self, channel):
        self.guessing_game_active = True
        self.game_channel = channel
        self.generate_answer()

    def end_game(self):
        self.guessing_game_active = False

    def add_guess(self, message):
        self.guesses[message.author] = message.content

    def check_for_winner(self):
        winner_list = []
        for key, value in self.guesses.items():
            if int(value) == self.answer:
                winner_list.append(key)
        if winner_list:
            return self.create_winner_message(winner_list)
        else:
            return "No one guessed the correct answer of: **{}**".format(self.answer)

    def create_winner_message(self, winner_list):
        if len(winner_list) > 1:
            return "The winners are: " + ",".join(winner_list)
        else:
            return "The winner is: {}".format(winner_list[0])
