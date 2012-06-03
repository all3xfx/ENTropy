from peewee import *

database = SqliteDatabase('characters.db')

class BaseModel(Model):
    class Meta:
        database = database

class Characters(BaseModel):
    name = CharField(unique = True)
    timesGuessed = IntegerField()
    
class Questions(BaseModel):
    question = TextField()
    
class Answers(BaseModel):
    character = ForeignKeyField(Characters)
    question = ForeignKeyField(Questions)
    answer = IntegerField()
    
class Weights(BaseModel):
    character = ForeignKeyField(Characters, related_name="weight")
    weight = DecimalField()

def createTables():
    Characters.create_table(True)
    Questions.create_table(True)
    Answers.create_table(True)
    Weights.create_table(True)
    
def addCharacters():
    f2 = open("characters.txt","r")
    
    f2.readline()
    
    data = []
    
    for line in f2:
        l = line.strip().split("\t")
        name = l[0]
        data.append(l[1:])
        Characters.get_or_create(name = name)
        
    f2.close()
    return data

def addQuestions():
    f = open("questions.txt", "r")
    
    questions = []
    for line in f:
        question = line.strip()
        Questions.get_or_create(question = question)
        
    f.close()
    
def addAnswers(data):
    qs = [q for q in Questions.select()]
    cs = [c for c in Characters.select()]
    
    for i in range(len(qs)):
        print qs[i].question
        for j in range(len(cs)):
            if i < 13:
                try:
                    data[j][i]
                except:
                    print "ERROR:", cs[j].name, data[j]
                Answers.get_or_create(character = cs[j], question = qs[i], answer=data[j][i])
            else:
                Answers.get_or_create(character=cs[j], question=qs[i])

"""createTables()
print "Questions..."
addQuestions()
print "Characters..."
c = addCharacters()
print "Answers..."
addAnswers(c)"""
