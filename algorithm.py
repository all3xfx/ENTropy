"""
Literature-themed 20 questions
by Veronica Lynn and Katherine Siegal
4 June 2012
"""


import math
import random
from db import Characters, Questions, Answers, database


class TwentyQuestions:

    def __init__(self):
        """Initializes the attributes for the given round."""

        self.cur_question = 0

        self.categories = Questions.select()

        self.answerPath = []

        self.likelyCharacter = None

        self.weights = {}

    def getEntropy(self, total):
        """Calculates the entropy for a given number of nodes. Because of how we're building our decision trees, there will always only be one yes."""

        # Avoid divide by zero/ log 0 errors
        if total <= 1:
            return 0

        p_y = float(1)/total
        p_n = 1 - p_y

        entropy = p_y*-math.log(p_y,2) + p_n*-math.log(p_n,2)
        return entropy

    def ask_question(self):
        """Decides which tree-building algorithm to use based on how far into the game it is"""

        self.cur_question += 1

        # Randomly select the first question to ask
        if self.cur_question == 1:
            #q = self.askFirstQuestion()
            randIndex = random.randint(1, Questions.select().count())
            while self.categories.where(id=randIndex).count() == 0:
                randIndex = random.randint(1, Questions.select().count())
            q = self.categories.get(id=randIndex)
            
        # Otherwise, build a decision tree to determine which question to ask next
        else:
            q = self.askAlg()
        return q

    def askFirstQuestion(self):
        """Chooses the first question to ask based on what splits the data most evenly. Doesn't actually get called currently."""

        bestApprox = 1
        bestCategory = None
        
        # For each question, calculate what fraction of the data is yes. Unknowns count as both yes and no, so factor those in, too.
        for category in self.categories:
            numYes = Answers.filter(question=category).filter(answer__gte=1).count()
            numUnknown = Answers.filter(question=category).filter(answer=0).count()
            fracYes = float(numYes + numUnknown)/(Characters.select().count()+2*numUnknown)

            # Find how close this fraction is from .5, which means it's a perfectly even split. Choose whichever question best approximates this.
            distFromHalf = abs(fracYes - .5)
            if distFromHalf < bestApprox:
                bestApprox = distFromHalf
                bestCategory = category
        return bestCategory

    def askAlg(self):
        """Chooses the optimal question by finding the next level of a decision tree. The tree that it constructs attempts to answer the question, 'Is is self.likelyCharacter'"""

        maxInfoGain = 0
        bestQuestion = None

        # Iterate through all the unasked questions to find the best one
        for question in self.categories:
            if Answers.filter(question=question).filter(character=self.likelyCharacter).count() > 0:
                answer = Answers.select().get(question=question, character=self.likelyCharacter).answer

                # We only want to consider questions where the most likely character's answer to that question is known
                if answer != 0:
                    # Figure out of the most likely character's answer to this question is yes or no
                    if answer >= 1:
                        child = Answers.filter(question=question).filter(answer__gte=1).count()
                    else:
                        child = Answers.filter(question=question).filter(answer__lte=1).count()
                    
                    # Calculate the information gain of this split. Choose the question with the highest info gain
                    total = Characters.select().count()
                    infoGain = self.getEntropy(total) - self.getEntropy(child)*child/total
                    if infoGain >= maxInfoGain:
                        maxInfoGain = infoGain
                        bestQuestion = question

        # If no question has been chosen, randomly choose one from the unasked questions (this happens when, for all questions left to ask, the most likely character's answer is unknown)
        if not bestQuestion:
            randIndex = random.randint(1, Questions.select().count())
            while self.categories.where(id=randIndex).count() == 0:
                randIndex = random.randint(1, Questions.select().count())
            bestQuestion = self.categories.get(id=randIndex)
        return bestQuestion

    def answer_question(self, question, answer):
        """Updates the question-and-answer path and adjusts the weights for each possible character."""

        greatestWeight = 0
        mostLikelyChar = self.likelyCharacter
        
        # Add question/answer pair to the list of all questions/answers this session
        self.answerPath.append((question,answer))
        
        # Remove the previously asked question from consideration in the future
        self.categories = self.categories.filter(question__ne=question.question)

        # For each character, update their weight (how likely they are to be the solution)
        for character in Characters.select():
            value = Answers.select().get(character=character, question=question).answer
            if character.name not in self.weights:
                self.weights[character.name] = float(character.timesGuessed)/Characters.select().count()

            # If the answer to the previous question was yes, add the character's numeric association with that question to the weight. If the answer was no, subtract it.
            if answer.lower() == "y" or answer.lower() == "yes":
                self.weights[character.name] += value
            elif answer.lower() == "n" or answer.lower() == "no":
                self.weights[character.name] -= value

            # The character with the highest weight is our current most likely character
            if self.weights[character.name] > greatestWeight:
                greatestWeight = self.weights[character.name]
                mostLikelyChar = character

    def guess(self):
        """Guesses the character that is our best guess at the time"""
        
        return self.likelyCharacter.name

    def process_results(self, answer):
        """Called once twenty questions is over. If the correct answer was guessed, increment the counter in the database representing the number of times that answer has been thought of before. If the incorrect answer was guessed, add that entry to the database."""

        # If the program guessed correctly, increment the database's counter for the number of times this character has been the solution
        if answer.lower() == "yes" or answer.lower() == "y":
            character = self.likelyCharacter
            character.timesGuessed += 1
            character.save()
            
        # If no, find out what the correct solution was
        else:
            name = raw_input("What is the name of the character you were thinking of? ")
            book = raw_input("What book are they from? ")

            new_entry = "{} ({})".format(name, book)
            try:
                # If this character already exists in the database (it just wasn't correctly guessed), update its counter for the number of times it has been the solution
                character = Characters.get(name = new_entry)
                character.timesGuessed += 1
                character.save()
            except Characters.DoesNotExist:
                # If the character is not in the database, add it
                character = Characters.create(name=new_entry, timesGuessed=1)

                for question in Questions.select():
                        Answers.create(question = question, character = character, answer=0)

        # Whether the program was right or wrong, update the database entry for the correct character and increment (if yes) or decrement (if no) its association with the questions that were asked
        for a in self.answerPath:
            question = a[0]
            response = a[1]

            q = Answers.get(question=question, character=character)

            if response.lower() == "yes" or response.lower() == "y":
                q.answer += 1
            elif response.lower() == "no" or response.lower() == "n":
                q.answer -= 1
            q.save()


    def run(self):
        """Where stuff happens!"""

        print " " + "_" * 48
        print "| ENTropy - 20 Questions for Literary Characters |"
        print "|" + "by Katherine Siegal & Veronica Lynn".center(48) + "|"
        print " " + "_" * 48
        print

        for i in range(20):
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
