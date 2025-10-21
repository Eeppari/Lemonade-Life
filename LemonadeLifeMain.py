import LemonadeLifeLibrary as LLlib
from random import choice, choices, randrange
from decimal import Decimal
from collections import Counter

class Business:
    nextid = 0
    def __init__(self, owner, name: str, business_type: str):
        self.owner : Player|Rival = owner
        self.name : str = name
        self.type : str = business_type
        self.id : int = Business.nextid
        self.workers : list = []
        self.max_customers: int = 0
        self.stock : dict = {}
        self.sellable_items : list = []
        Business.nextid += 1
    
    def set_owner(self, newOwner):
        self.owner = newOwner

    def get_id(self) -> int:
        return self.id
    
    def get_type(self) -> str:
        return self.type

    def get_workers(self) -> list:
        return self.workers
    
    def get_worker_amount(self) -> int:
        return len(self.workers)
    
    def get_worker_sell_power(self) -> int:
        return self.get_worker_amount() * 10
    
    def append_to_work(self, worker: "Entity"):
        self.workers.append(worker)

    def remove_from_work(self, worker: "Entity"):
        self.workers.remove(worker)

    def buy_stock(self, market, item = None, amount = None) -> None:
        market : Market = market
        buyer_ent : Entity = self.owner
        if not issubclass(type(buyer_ent), (NPC, Player)):
            return
        if type(buyer_ent) == Player:
            print("What do you need:")
            for i in [x for x in self.stock if x in market.get_buy_items()]:
                print(f"\t-{i.capitalize()} {market.get_buy_price(i)}€")
            print(f"You have {buyer_ent.get_money()}€")
        
        if item == None:
            item = input("Item:\n->")
        if amount == None:
            while amount == None or not amount.isdigit():
                    amount = input("Amount:\n->")
        buy_price: int = round(market.get_buy_price(item) * int(amount), 1)
        if buy_price == None or not item in self.stock:
            print("Invalid item")
            return
        if buyer_ent.get_money() >= buy_price:
            if type(buyer_ent) == Player:
                print(f"You bought {amount} {item} for {buy_price}€")
            buyer_ent.change_money(buy_price * -1)
            self.stock[item] += int(amount)
        else:
            if type(buyer_ent) == Player:
                print(f"You cannot afford the purchase of {amount} {item} for {buy_price}€.\nYou have {buyer_ent.get_money()}€")
    
    def sell(self, item):
        print("Sold")

    def run_business(self, market):
        print("This business doesnt work yet")
    
class LemonadeStand(Business):
    def __init__(self, owner, name = "Lemonade Shop"):
        super().__init__(owner=owner, name=name, business_type="lemonade stand")
        self.max_customers = 50
        self.sellable_items: list = [
            "lemonade",
        ] 
        self.stock = {
            "lemon" : 0,
            "lemonade" : 0,
        }

    def __str__(self):
        return self.name
    
    def get_stock(self):
        return self.stock

    def run_business(self, market:"Market"):
        print("Running: run_business")
        #Check how many customers
        coming_customers : int = self.get_worker_sell_power() if self.get_worker_sell_power() <= self.max_customers else self.max_customers
        max_orders = 4
        orders: dict = dict(Counter(choices(self.sellable_items, k=max_orders*coming_customers)))
        for x in orders:
            if self.stock[x] <= 0:
                can_sell = 0
                print(f"You are out of {x}")
            else:
                can_sell : int = orders[x] if orders[x] < self.stock[x] else self.stock[x]
            orders_price: int = market.get_sell_price(x) * can_sell
            if self.stock[x] > 0:
                print(f"You sold {can_sell} {x} for {orders_price}€")
            if can_sell == self.stock[x] and self.stock[x] != 0:
                print(f"You ran out of {x}")
            self.owner.change_money(orders_price)
            self.stock[x] -= can_sell


    def make_lemonade(self):
        if self.stock["lemon"] >= 1:
            self.stock["lemonade"] += 10 + (10 * self.get_worker_amount()) if self.stock["lemon"] >= 10 + (10 * self.get_worker_amount()) else self.stock["lemon"]
            self.stock["lemon"] -= 10 + (10 * self.get_worker_amount()) if self.stock["lemon"] >= 10 + (10 * self.get_worker_amount()) else self.stock["lemon"]
        else:
            print("You don't have enough lemons to make lemonade")
        
    def sell_lemonade(self, market) -> None: #Can be changed to Business class
        if self.stock["lemonade"] >= 1:
            self.stock["lemonade"] -= 1
            self.owner.change_money(market.get_sell_price("lemonade"))
        else:
            print("You don't have any lemonade!")
    
    def show_stock(self):
        print(f"{self.name} has:")
        for x in self.stock:
            print(f"\t{x} - {self.stock[x]}")
        input("(enter anything to continue)\n->")
    
    def doActions(self, market):
        all_actions = Game.check_actions("lemonade_stand")
        for i in range(len(all_actions)):
            print(f"{i+1}. {all_actions[i+1]}")
        action = int(input("->"))
        actionFunction = {
            "work in business" : (lambda: self.append_to_work(self.owner), 1),
            "buy stock" : (lambda: self.buy_stock(market=market), 1), #self.buy_stock(market=market)
            "make lemonade" : (self.make_lemonade, 1),
            "sell lemonade" : (self.sell_lemonade, 1),
            "show" : (self.show_stock, 0),
            }
        if action in all_actions:
            actionFunction[all_actions[action]][0]()
            return actionFunction[all_actions[action]][1]
        return 0

#ENTITIES
class Entity:
    def __init__(self, fName, lName: str, age: int, money: int = 0):
        self.fName : str = fName
        self.lName : str = lName
        self.age : int = age
        self.money : int = money

    def get_money(self) -> int:
        return self.money
    
    def set_money(self, amount:int) -> None:
        self.money = amount

    def change_money(self, amount:int) -> None:
        self.money += amount

    def __str__(self):
        return f"{self.fName} {self.lName}"

class Player(Entity):
    def __init__(self, fName, lName, age = 18):
        self.money : int = 0
        super().__init__(fName=fName, lName=lName, age=age, money=self.money)
        self.ownedBusinesses: list[Business] = []

    def get_owned_businesses(self) -> list:
        return self.ownedBusinesses

class NPC(Entity):
    def __init__(self, fName = None, lName = None, age = 18, gender = choice(["M", "F"]), money = None):
        fName = fName if fName != None else self.generate_npc_fname(gender=gender)
        lName = lName if lName != None else self.generate_npc_lname()
        self.money = money if money != None else randrange(100, 1000)
        super().__init__(fName=fName, lName=lName, age=age, money=self.money)
    
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

    def get_owned_businesses(self) -> list:
        return self.ownedBusinesses

    def badWord(self):
        print("BADWORD")

class Citizen(NPC):
    def buy(self):
        print("BUY")

class Market:
    def __init__(self):
        self.buy_prices: dict[str, int|float] = {
            "lemon": 0.5,
            "banana": 0
        }
        self.sell_prices: dict[str, int|float] = {
            "lemonade": 1,
        }
        for x in self.buy_prices:
            if not x in self.sell_prices: 
                self.sell_prices[x] = round(self.buy_prices[x]/1.5, 1)

    def get_buy_price(self, item):
        return self.buy_prices[item] if item in self.buy_prices else None
    
    def get_sell_price(self, item):
        return self.sell_prices[item] if item in self.sell_prices else None
    
    def get_buy_items(self):
        return self.buy_prices.keys()
    
    def count_price(self, item, quantity):
        pass


#GAME MANAGER
class GameManager:
    def __init__(self, entities, market: Market, game_lenght: int = -1):
        self.days = 0
        self.p_energy = 5
        self.entities = entities
        self.citizens = [i for i in entities if type(i) == Citizen]
        self.rivals = [i for i in entities if type(i) == Rival]
        self.mainPlayer = self.findPlayer()
        self.market = market

    def start(self):
        self.mainPlayer.ownedBusinesses.append(LemonadeStand(self.mainPlayer))
        self.mainPlayer.money = 100
    
    def next_day(self):
        self.days += 1
        print(f"\n\n\tDay {self.days}".center(20))
        for x in self.entities:
            if x is self.mainPlayer:
                continue
            x.money += 1
        energy = 1
        while energy > 0:
            #Actions
            print(("-----" * 5).center(22))
            while True:
                avaibleActions = self.check_actions("player")
                for i in range(len(avaibleActions)):
                    print(f"{i+1}. {avaibleActions[i+1]}")
                while True:
                    action = input("->")
                    if action.isdigit() and int(action) in avaibleActions:
                        action = avaibleActions[int(action)]
                        break
                    else:
                        if not action.isdigit():
                            print("Input not right. Has to be an intereger.\nTry again.")
                        elif not int(action) in avaibleActions:
                            print("Input not right. Has to be in actions listed.\nTry again.")
                
                energy -= self.doAction(action)
                self.simulateTime()
                break

    def simulateTime(self):
        for businessEnt in [self.mainPlayer] + self.rivals:
            #Check businesses
            for business in businessEnt.get_owned_businesses():
                self.check_business(business)
    
    def check_business(self, target: Business):
        if target.get_worker_amount() > 0:
            target.run_business(market=self.market)
            if target.owner in target.get_workers():
                target.remove_from_work(target.owner)

    def findPlayer(self):
        for x in entities:
            if type(x) == Player:
                return x
        raise

    def check_actions(self, actionsType):
        actionList = []
        if actionsType == "player":
            actionList.append(f"{self.mainPlayer}")
            if self.mainPlayer.ownedBusinesses:
                actionList.append("Manage businesses")
            if self.rivals:
                actionList.append("See rivals")

        elif actionsType == "all_businesses_player":
            for x in self.mainPlayer.ownedBusinesses:
                actionList.append(x)

        elif actionsType == "lemonade_stand":
            actionList.append("work in business")
            actionList.append("buy stock")
            actionList.append("make lemonade")
            actionList.append("sell lemonade")
            actionList.append("show")

        else:
            print(f"Wrong type of actions for checking actions.\n>Got for actionsType : {actionsType}<")
            raise
        return dict(enumerate(actionList, 1))
    
    def doAction(self, action):
        def manage_businesses():
            all_businesses = self.check_actions("all_businesses_player")
            for i in range(len(all_businesses)):
                print(f"{i+1}. {str(all_businesses[i+1])}")
            while True:
                targ_business = input("->")
                if targ_business.isdigit() and int(targ_business) in all_businesses:
                    targ_business = all_businesses[int(targ_business)]
                    break
                elif targ_business == "":
                    return
                else:
                    print("Invalid number.\nTry again.")
            return targ_business.doActions(self.market)
        
        def own_stats():
            targetEnt = self.mainPlayer
            stats_to_show = {
                "age" : targetEnt.age,
                "money" : targetEnt.get_money(),
                "owned businesses" : targetEnt.ownedBusinesses
            }
            print(f"\n\n{targetEnt.fName} {targetEnt.lName}:")
            for stat in stats_to_show:
                if not stat in ["owned businesses"]:
                    print(f"\t{stat.capitalize()}: {stats_to_show[stat]}")
                elif stat == "owned businesses":
                    print("Owned businesses:")
                    sorted_businesses = []
                    for x in stats_to_show["owned businesses"]:
                        sorted_businesses.append({"name":x.name, "business_object": x, "business_id":x.get_id()})
                    sorted_businesses.sort(key=LLlib.get_name_var_from_dict)
                    for b in sorted_businesses:
                        print(f"\t{b["name"]} ({b["business_object"].get_type()}, id:{b["business_id"]})")
            input("(enter anything to continue)\n->")
            return 0

        actionFunction = {
            f"{self.mainPlayer}" : own_stats,
            "Manage businesses" : manage_businesses,
        }
        if action in actionFunction:
            return actionFunction[action]()
        return 0

    def buy_Bussines(self, buyer, bussinesType):
        print(f"{buyer} is buying {bussinesType}")

entities = [Player("Eetu", "Rutanen", 15), Citizen(), Citizen(), Rival(), Rival()]
Game = GameManager(entities=entities, market=Market())
Game.start()
for x in Game.entities:
    print(x)
    if type(x) != Citizen:
        print(x.ownedBusinesses)
    if issubclass(type(x), NPC) == True:
        print("Is a NPC")

TestRun = False #if you need to make test and skip the game

#TESTS
if TestRun:
    exit()
#GAME
for i in range(10):
    Game.next_day()
