"""
Literature-themed 20 questions
by Veronica Lynn and Katherine Siegal
4 June 2012
"""


import math
from db import *

class TwentyQuestions:

    def __init__(self):
        self.cur_question = 0

        self.categories = Questions.select()

        self.answerPath = []

        Weights.drop_table(True)
        Weights.create_table()

        for character in Characters.select():
            chance = float(character.timesGuessed)/Characters.select().count()
            Weights.get_or_create(character=character, weight=chance)

    def getEntropy(self):
        return

    def ask_question(self):
        """Decides which tree-building algorithm to use based on how far into the game it is"""

        self.cur_question += 1

        if self.cur_question == 1:
            q = self.askFirstQuestion
        else:
            q = self.askAlg
        return q

    def askFirstQuestion(self):
        """Chooses the first question to ask based on what splits the data most evenly."""
        bestApprox = 1
        bestCategory = 0

        for category in self.categories:
            numYes = Answers.filter(question=category).filter(answer__gte=1).count()
            numUnknown = Answers.filter(question=category).filter(answer=0).count()
            fracYes = float(numYes + numUnknown)/(Characters.select().count()+2*numUnknown)

            distfromHalf = abs(fracYes - .5)
            if distFromHalf < bestApprox:
                bestApprox = distFromHalf
                bestCategory = category

        return category

    def askAlg(self):
        """Chooses the optimal question..."""


    def answer_question(self, question, answer):
        self.answerPath.append((question,answer))
        self.categories = self.categories.filter(question__ne=question.question)
        if answer == "Y":



    def guess(self):
        return [item[0] for item in self.data]

    def process_results(self, answer):
        """Called once twenty questions is over. If the correct answer was guessed, increment the counter in the database representing the number of times that answer has been thought of before. If the incorrect answer was guessed, add that entry to the database."""

        if answer == "Y":
            pass
        else:
            name = raw_input("What is the name of the character you were thinking of? ")
            book = raw_input("What book are they from? ")

    def run(self):
        print " " + "_" * 48
        print "| ENTropy - 20 Questions for Literary Characters |"
        print "|" + "by Katherine Siegal & Veronica Lynn".center(48) + "|"
        print " " + "_" * 48
        print
        for i in range(5):
            question = self.ask_question()
            a = raw_input("{}) {} ".format(i + 1, question.question))
            print
            self.answer_question(question,a)

        print "WERE YOU THINKING OF..."
        print self.guess()
        a = raw_input("Y or N: ")
        self.process_results(a)

# For running from the command line
if __name__ == "__main__":
    twentyqs = TwentyQuestions()
    twentyqs.run()
