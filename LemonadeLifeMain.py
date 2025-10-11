import LemonadeLifeLibrary as LLlib
from random import choice, randrange

class Business:
    def __init__(self, owner):
        self.owner = owner
    
    def set_owner(self, newOwner):
        self.owner = newOwner
    
    def sell(self):
        print("SOLD")
    
class LemonadeStand(Business):
    def __init__(self, owner, name = "Lemonade Shop"):
        super().__init__(owner=owner)
        self.name = name
        self.stock = {
            "Lemon" : 0,
            "Lemonade" : 0
        }

    def __str__(self):
        return self.name

    def buy_stock(self):
        self.stock["Lemon"] += 1

    def make_lemonade(self):
        self.stock["Lemonade"] += 1
        self.stock["Lemon"] -= 1

    def get_stock(self):
        return self.stock
    
    def doActions(self):
        all_actions = Game.check_actions("lemonade_stand")
        for i in range(len(all_actions)):
            print(f"{i+1}. {all_actions[i+1]}")
        action = int(input("::"))
        if all_actions[action] == "buy stock":
            self.buy_stock()
        elif all_actions[action] == "make lemonade":
            self.make_lemonade()
        elif all_actions[action] == "show":
            print(self.get_stock())


#ENTITIES
class Player:
    def __init__(self, fName, lName, age = 18):
        self.fName : str = fName
        self.lName : str = lName
        self.age : int = age
        self.ownedBusinesses: list[Business] = []
        self.money : int = 0

    def __str__(self):
        return f"{self.fName} {self.lName}"
    
    def get_money(self) -> int:
        return self.money
    def set_money(self, amount:int) -> None:
        self.money = amount
    def change_money(self, amount:int) -> None:
        self.money += amount

class NPC:
    def __init__(self, fName = None, lName = None, age = 18, gender = choice(["M", "F"]), money = None):
        self.fName = fName if fName != None else self.generate_npc_fname(gender=gender)
        self.lName = lName if lName != None else self.generate_npc_lname()
        self.age = age
        self.money = money if money != None else randrange(100, 1000)

    def __str__(self):
        return f"{self.fName} {self.lName}"
    
    def generate_npc_fname(self, gender):
        if gender.lower() == "f":
            return choice(LLlib.get_girl_name_list())
        else:
            return choice(LLlib.get_boy_name_list())
    
    def generate_npc_lname(self):
        return choice(LLlib.generate_last_name())

class Rival(NPC):
    def __init__(self, fName = None, lName = None, age = 18):
        super().__init__(fName=fName, lName=lName, age=age)
        self.ownedBusinesses: list[Business] = []

    def badWord(self):
        print("BADWORD")

class Citizen(NPC):
    def buy(self):
        print("BUY")


#GAME MANAGER
class GameManager:
    def __init__(self, entities):
        self.days = 0
        self.entities = entities
        self.citizens = [i for i in entities if type(i) == Citizen]
        self.rivals = [i for i in entities if type(i) == Rival]
        self.mainPlayer = self.findPlayer()

    def start(self):
        self.mainPlayer.ownedBusinesses.append(LemonadeStand(self.mainPlayer))
        self.mainPlayer.money = 100
    
    def next_day(self):
        self.days += 1
        print(f"\n\n\tDay {self.days}".center(20))
        print(("-----" * 5).center(22))
        for x in self.entities:
            if x is self.mainPlayer:
                continue
            x.money += 1

        #Actions
        while True:
            avaibleActions = self.check_actions("player")
            for i in range(len(avaibleActions)):
                print(f"{i+1}. {avaibleActions[i+1]}")
            while True:
                action = input("::")
                if action.isdigit() and int(action) in avaibleActions:
                    action = avaibleActions[int(action)]
                    break
                else:
                    if not action.isdigit():
                        print("Input not right. Has to be an intereger.\nTry again.")
                    elif not int(action) in avaibleActions:
                        print("Input not right. Has to be in actions listed.\nTry again.")
            
            self.doAction(action)
            break
    
    def findPlayer(self):
        for x in entities:
            if type(x) == Player:
                return x
        raise

    def check_actions(self, actionsType):
        actionList = []
        if actionsType == "player":
            if self.mainPlayer.ownedBusinesses:
                actionList.append("See businesses")
            if self.rivals:
                actionList.append("See rivals")
        elif actionsType == "all_businesses_player":
            for x in self.mainPlayer.ownedBusinesses:
                actionList.append(x)
        elif actionsType == "lemonade_stand":
            actionList.append("buy stock")
            actionList.append("make lemonade")
            actionList.append("show")
        else:
            print(f"Wrong type of actions for checking actions.\n>Got for actionsType : {actionsType}<")
            raise
        return dict(enumerate(actionList, 1))
    
    def doAction(self, action):
        def see_businesses():
            all_businesses = self.check_actions("all_businesses_player")
            for i in range(len(all_businesses)):
                print(f"{i+1}. {str(all_businesses[i+1])}")
            targ_business = all_businesses[int(input("::"))]
            targ_business.doActions()
            

        actionFunction = {
            "See businesses" : see_businesses,
        }
        if action in actionFunction:
            actionFunction[action]()

    def buy_Bussines(self, buyer, bussinesType):
        print(f"{buyer} is buying {bussinesType}")

entities = [Player("Eetu", "Rutanen", 15), Citizen(), Citizen(), Rival()]
Game = GameManager(entities=entities)
Game.start()
for x in Game.entities:
    print(x)
    if type(x) != Citizen:
        print(x.ownedBusinesses)

for i in range(10):
    Game.next_day()
