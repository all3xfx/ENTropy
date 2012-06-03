"""
Literature-themed 20 questions
by Veronica Lynn and Katherine Siegal
4 June 2012
"""


import math
from db import *

class TwentyQuestions:

    def __init__(self):
        self.get_data()

        self.cur_question = 0

        self.categories = Questions.select()

        self.answerPath = []

    def get_data(self):
        self.data = []

        f = open("characters.txt","r")

        self.categories = f.readline().strip().split("\t")[1:]
        for line in f:
            l = line.strip().split("\t")
            entry = (l[0], l[1:])
            self.data.append(entry)
        f.close()

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
        self.categories = self.categories.filter(question__ne=category.question)
        return category.question

    def askAlg(self):
        """Chooses the optimal question..."""


    def answer_question(self, answer):


        for item in self.data:
            index = self.categories.index(self.cur_category)
            if item[1][index] == answer:
                new.append(item)
         self.data = new

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
        print "|" + "by Katherine Siegal & Veronica Lynn".center(48)  + "|"
        print " " + "_" * 48
        print
        for i in range(5):
            a = raw_input("{}) {} ".format(i + 1, self.ask_question()))
            print
            self.answer_question(a)

        print "WERE YOU THINKING OF..."
        print self.guess()
        a = raw_input("Y or N: ")
        self.process_results(a)

# For running from the command line
if __name__ == "__main__":
    twentyqs = TwentyQuestions()
    twentyqs.run()

