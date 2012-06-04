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
