import LemonadeLifeLibrary as LLlib
from random import choice

class Busines:
    def __init__(self, moneyM, owner):
        self.moneyMade = moneyM
        self.owner = owner
    
    def set_owner(self, newOwner):
        self.owner = newOwner
    
    def sell(self):
        print("SOLD")
    
class LemonadeStand(Busines):
    def __init__(self, moneyM, Lemonades):
        super().__init__(moneyM)
        self.Lemonades = Lemonades

class Player:
    def __init__(self, fName, lName, age = 18):
        self.fName = fName
        self.LName = lName
        self.age = age
        self.ownedBusinesses = []
        self.money = 0

class NPC:
    def __init__(self, fName = None, lName = None, age = 18, gender = choice(["M", "F"])):
        self.fName = fName if fName != None else self.generate_npc_fname(gender=gender)
        self.LName = lName if lName != None else self.generate_npc_lname()
        self.age = age

    def __str__(self):
        return f"{self.fName, self.LName}"
    
    def generate_npc_fname(self, gender):
        if gender.lower() == "f":
            return choice(LLlib.get_girl_name_list())
        else:
            return choice(LLlib.get_boy_name_list())
    
    def generate_npc_lname(self):
        return choice(LLlib.generate_last_name())

class Rival(NPC):
    def badWord(self):
        print("BADWORD")

class Citizen(NPC):
    def buy(self):
        print("BUY")

class GameManager:
    def __init__(self, entities):
        self.days = 0
        self.entities = entities

    def buy_Bussines(self, buyer, bussinesType):
        print(f"{buyer} is buying {bussinesType}")

entities = [Player("Eetu", "Rutanen", 15), Citizen(lName="Kari"), Citizen()]
Game = GameManager(entities=entities)
for x in Game.entities:
    print(x)