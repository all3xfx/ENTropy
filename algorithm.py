class TwentyQuestions:
   
    def __init__(self):      
        self.data = self.get_data()
        
        self.cur_question = 0

    def get_data(self):
        return
    
    def getEntropy(self):
        return

    def ask_question(self):
        """Decides which tree-building algorithm to use based on how far into the game it is"""
        
        self.cur_question += 1
        
        if self.cur_question < 2:
            q = self.ask_alg1()
        else:
            q = self.ask_alg2()
        return q
        
    def ask_alg1(self):
        """Choose the questions that split the data (approximately) in half so as to optimally narrow down the possible solutions."""
        
        return "Is it human?"
        
    def ask_alg2(self):
        return "Does it have four hooves, a horn, and a tail?"
        
    def answer_question(self, answer):
        pass
        
    def guess(self):
        return "ponies"
        
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
        for i in range(2):
            a = raw_input("{}) {} ".format(i + 1, self.ask_question()))
            print
            self.answer_question(a)
        
        print "WERE YOU THINKING OF..."
        print self.guess() + "?"
        a = raw_input("Y or N: ")
        self.process_results(a)

# For running from the command line
if __name__ == "__main__":
    twentyqs = TwentyQuestions()
    twentyqs.run()
        
