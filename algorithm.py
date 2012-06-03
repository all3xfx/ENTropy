"""
Literature-themed 20 questions
by Veronica Lynn and Katherine Siegal
4 June 2012
"""


import math
from db import *
from time import time


class TwentyQuestions:

    def __init__(self):
        """Initializes the attributes for the given round."""

        self.cur_question = 0

        self.categories = Questions.select()

        self.answerPath = []

        self.likelyCharacter = 0

    def getEntropy(self, total):
        """Docstrings here, get yer docstrings!"""

        p_y = float(1)/total
        p_n = 1 - p_y
        entropy = p_y*-math.log(p_y,2) + p_n*-math.log(p_n,2)
        return entropy

    def ask_question(self):
        """Decides which tree-building algorithm to use based on how far into the game it is"""

        self.cur_question += 1

        if self.cur_question == 1:
            q = self.askFirstQuestion()
        else:
            q = self.askAlg()
        return q

    def askFirstQuestion(self):
        """Chooses the first question to ask based on what splits the data most evenly."""
        bestApprox = 1
        bestCategory = 0
        
        t1 = time()
        for category in self.categories:
            numYes = Answers.filter(question=category).filter(answer__gte=1).count()
            numUnknown = Answers.filter(question=category).filter(answer=0).count()
            fracYes = float(numYes + numUnknown)/(Characters.select().count()+2*numUnknown)

            distFromHalf = abs(fracYes - .5)
            if distFromHalf < bestApprox:
                bestApprox = distFromHalf
                bestCategory = category
        t2 = time()
        print "Ask first:", t2-t1
        return bestCategory

    def askAlg(self):
        """Chooses the optimal question..."""

        maxInfoGain = 0
        bestQuestion = 0

        t1 = time()
        for question in self.categories:
            if Answers.filter(question=question).filter(character=self.likelyCharacter).count() > 0:
                answer = Answers.select().get(question=question, character=self.likelyCharacter).answer

                if answer != 0:
                    if answer >= 1:
                        child = Answers.filter(question=question).filter(answer__gte=1).count()
                    else:
                        child = Answers.filter(question=question).filter(answer__lte=1).count()
                    total = Characters.select().count()

                    infoGain = self.getEntropy(total) - self.getEntropy(child)*child/total
                    if infoGain >= maxInfoGain:
                        maxInfoGain = infoGain
                        bestQuestion = question

        t2 = time()
        print "Ask next:", t2-t1
        return bestQuestion

    def answer_question(self, question, answer):
        """Updates the question-and-answer path and adjusts the weights for each possible character."""

        greatestWeight = 0
        mostLikelyChar = 0
        self.answerPath.append((question,answer))
        self.categories = self.categories.filter(question__ne=question.question)

        t1 = time()
        for character in Characters.select():
            value = Answers.select().get(character=character, question=question).answer
            weight = Weights.select().get(character=character)
            if self.cur_question == 1:
                weight.weight = float(character.timesGuessed)/Characters.select().count()

            if answer == "Y":
                weight.weight += value
            elif answer == "N":
                weight.weight -= value
            weight.save()

            if weight.weight > greatestWeight:
                greatestWeight = weight.weight
                mostLikelyChar = character

        self.likelyCharacter = mostLikelyChar
        t2 = time()
        print "Answer question:", t2-t1

    def guess(self):
        return self.likelyCharacter.name

    def process_results(self, answer):
        """Called once twenty questions is over. If the correct answer was guessed, increment the counter in the database representing the number of times that answer has been thought of before. If the incorrect answer was guessed, add that entry to the database."""

        if answer == "Y":
            pass
        else:
            name = raw_input("What is the name of the character you were thinking of? ")
            book = raw_input("What book are they from? ")

    def run(self):
        """Where stuff happens!"""

        print " " + "_" * 48
        print "| ENTropy - 20 Questions for Literary Characters |"
        print "|" + "by Katherine Siegal & Veronica Lynn".center(48) + "|"
        print " " + "_" * 48
        print

        for i in range(4):
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
