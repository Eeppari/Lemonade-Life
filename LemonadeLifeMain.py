import LemonadeLifeLibrary as LLlib
from random import choice, choices, randrange
from decimal import Decimal
from collections import Counter
from time import sleep

class Business:
    nextId = 0
    def __init__(self, owner, name: str, business_type: str):
        self.owner : Player|Rival = owner
        self.name : str = name
        self.type : str = business_type
        self.id : int = Business.nextId
        self.workers : list = []
        self.bills : dict[str, function] = {
            "wages" : self.get_wages,
        }
        self.max_customers: int = 0
        self.stock : dict = {}
        self.sellable_items : list = []
        Business.nextId += 1
    
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
    
    def get_max_worker_amount(self) -> int:
        print("This has not been done yet")
        raise
    
    def get_worker_sell_power(self) -> int:
        return self.get_worker_amount() * 10
    
    def append_to_work(self, worker: "Entity"):
        self.workers.append(worker)

    def remove_from_work(self, worker: "Entity"):
        self.workers.remove(worker)

    def get_wages(self):
        return self.get_worker_amount() * 3
    
    def get_bills(self, specification: str = "all"):
        """
        Bills types are
        all -> all of the bills,
        wages -> combined wages of all of the workers in the business
        """
        if specification != "all" and specification in self.bills:
            return self.bills[specification]()
        else:
            return self.bills

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
        #Check how many customers
        coming_customers: int = randrange(self.get_worker_sell_power() - self.get_worker_amount(), self.get_worker_sell_power() +1 ) if self.get_worker_sell_power() <= self.max_customers else self.max_customers
        max_orders: int = 4
        orders_amount: int = sum(randrange(1, max_orders) for x in range(coming_customers))
        orders: dict = dict(Counter(choices(self.sellable_items, k=orders_amount)))
        for x in orders:
            if self.stock[x] <= 0:
                can_sell = 0
                print(f"{self.name} is out of {x}")
            else:
                can_sell : int = orders[x] if orders[x] < self.stock[x] else self.stock[x]
            orders_price: int = market.get_sell_price(x) * can_sell
            if self.stock[x] > 0:
                print(f"{self.name} sold {can_sell} {x} for {orders_price}€")
            if can_sell == self.stock[x] and self.stock[x] != 0:
                print(f"{self.name} ran out of {x}")
            self.owner.change_money(orders_price)
            self.stock[x] -= can_sell


    def make_lemonade(self) -> None:
        #Does not consume energy but takes time to make lemonade
        #Make time like 1s
        if self.stock["lemon"] >= 1:
            print("Making lemonade...")
            sleep(1)
            lemonade_made = 10 + (10 * self.get_worker_amount()) if self.stock["lemon"] >= 10 + (10 * self.get_worker_amount()) else self.stock["lemon"]
            self.stock["lemonade"] += lemonade_made
            self.stock["lemon"] -= lemonade_made
            print(f"Made {lemonade_made} lemonade")
            sleep(0.5)
        else:
            print("You don't have enough lemons to make lemonade")
            LLlib.input_anything_to_continue()
    
    def show_stock(self):
        print(f"{self.name} has:")
        for x in self.stock:
            print(f"\t{x} - {self.stock[x]}")
        LLlib.input_anything_to_continue()
    
    def doActions(self, market):
        all_actions = Game.check_actions("lemonade_stand")
        print(f"{self.name}:")
        for i in range(len(all_actions)):
            print(f"{i+1}. {all_actions[i+1]}")
        action = int(input("->"))
        actionFunction = {
            "work in business" : (lambda: self.append_to_work(self.owner), 1),
            "buy stock" : (lambda: self.buy_stock(market=market), 0), #self.buy_stock(market=market)
            "make lemonade" : (self.make_lemonade, 0),
            "show" : (self.show_stock, 0),
            }
        if action in all_actions:
            actionFunction[all_actions[action]][0]()
            return actionFunction[all_actions[action]][1]
        return 0

#ENTITIES
class Entity:
    nextEntId: int = 0
    def __init__(self, fName, lName: str, age: int, money: int = 0):
        self.fName : str = fName
        self.lName : str = lName
        self.age : int = age
        self.money : int = money
        self.entId : int = Entity.nextEntId
        Entity.nextEntId += 1

    def get_money(self) -> int:
        return self.money
    
    def set_money(self, amount:int) -> None:
        self.money = amount

    def change_money(self, amount:int) -> None:
        self.money += amount

    def get_entity_id(self) -> int:
        return self.entId

    def __str__(self):
        return f"{self.fName} {self.lName}"

class Player(Entity):
    def __init__(self, fName, lName, age = 18):
        self.money : int = 0
        super().__init__(fName=fName, lName=lName, age=age, money=self.money)
        self.ownedBusinesses: list[Business] = []
        self.workers : list[Worker] = []

    def get_owned_businesses(self) -> list:
        return self.ownedBusinesses
    
    def get_workers(self) -> list:
        return self.workers

    def hire_worker(self) -> None:
        hired_worker = Worker()
        self.workers.append(hired_worker)
        print(f"You hired {hired_worker}")

    def fire_worker(self, workerToFire: "Worker", leftByOwn: bool = False) -> None:
        if workerToFire in self.workers:
            self.workers.remove(workerToFire)
            if not leftByOwn:
                print(f"You fired {workerToFire}")
        else:
            print("ERROR: Worker not found or doesn't work for this entity.")
            print(f"\tEntity gotten: {workerToFire}\n\t{self}'s workers: {[str(x) for x in self.workers]}")
            raise


class NPC(Entity):
    def __init__(self, fName = None, lName = None, age = 18, gender = None, money = None):
        if gender == None:
            gender = choice(["M", "F"])
        fName = fName if fName != None else self.generate_npc_fname(gender=gender)
        lName = lName if lName != None else self.generate_npc_lname()
        self.money = money if money != None else randrange(100, 1000)
        self.gender : str = gender
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
        self.workers : list[Worker] = []

    def get_owned_businesses(self) -> list:
        return self.ownedBusinesses
    
    def get_workers(self) -> list:
        return self.workers
    
    def hire_worker(self):
        hired_worker = Worker()
        self.workers.append(hired_worker)
        print(f"{self} hired {hired_worker}")

    def fire_worker(self, workerToFire: "Worker", leftByOwn: bool = False) -> None:
        if workerToFire in self.workers:
            self.workers.remove(workerToFire)
            if not leftByOwn:
                print(f"{self} fired {workerToFire}")
        else:
            print("ERROR: Worker not found or doesn't work for this entity.")
            print(f"\tEntity gotten: {workerToFire}\n\t{self}'s workers: {[str(x) for x in self.workers]}")
            raise        

    def badWord(self):
        print("BADWORD")

class Worker(NPC):
    def __init__(self, fName=None, lName=None, age=18, gender=None, money=None):
        super().__init__(fName, lName, age, gender, money)
        self.workBusiness = None

    def get_work_business(self) -> Business|None:
        return self.workBusiness
    
    def set_work_business(self, targBusiness: Business) -> None:
        self.workBusiness = targBusiness

    def remove_from_work_business(self):
        self.workBusiness = None

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
                break
        self.simulateTime()

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
                
            wages_to_pay = target.get_bills("wages")
            if target.owner.get_money() >= wages_to_pay:
                target.owner.change_money(wages_to_pay * -1)
                print(f"You paid {wages_to_pay}€ for wages in {target}")
            else:
                random_worker = choice(target.get_workers())
                target.owner.fire_worker(random_worker)
                target.remove_from_work(random_worker)
                print(f"{random_worker} has left becouse you do not have enough money to pay his wage")

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
                actionList.append("Manage workers")
            if self.rivals:
                actionList.append("See rivals")
        
        elif actionsType == "business_management":
            actionList.append("Create business")
            for x in self.mainPlayer.ownedBusinesses:
                actionList.append(x)

        elif actionsType == "all_businesses_player":
            for x in self.mainPlayer.ownedBusinesses:
                actionList.append(x)
        
        elif actionsType == "worker_management":
            actionList.append("Hire workers")
            if self.mainPlayer.workers != []:
                actionList.append("Append workers to business")
                actionList.append("Remove workers from business")


        elif actionsType == "lemonade_stand":
            actionList.append("work in business")
            actionList.append("buy stock")
            actionList.append("make lemonade")
            actionList.append("show")

        else:
            print(f"Wrong type of actions for checking actions.\n>Got for actionsType : {actionsType}<")
            raise
        return dict(enumerate(actionList, 1))
    
    def doAction(self, action):
        def manage_businesses():
            business_management_actions = self.check_actions("business_management")
            for i in range(len(business_management_actions)):
                print(f"{i+1}. {str(business_management_actions[i+1])}")
            targ_business: Business | str = LLlib.ask_for_digit_and_check_in_dict(business_management_actions)
            if issubclass(type(targ_business), Business):
                return targ_business.doActions(self.market)
            elif type(targ_business) == str:
                if targ_business == "Create business":
                    creating_cost = 1000
                    if self.mainPlayer.get_money() >= creating_cost:
                        if input(f"Creating a new business will cost {creating_cost}€. \nDo you want to create a business? (Y/N)").lower() == "y":
                            newBusinessName = input("Input the name for business\n-> ")
                            self.create_Business(self.mainPlayer, LemonadeStand, newBusinessName)
                            self.mainPlayer.change_money(creating_cost * -1)
                        else:
                            return 0
                    else:
                        print("You don't have enought money!")
                        return 0
                return 0
        
        def manage_workers():
            worker_management_actions = self.check_actions("worker_management")
            for i in range(len(worker_management_actions)): #List all of the possible actions in worker_management page
                print(f"{i+1}. {str(worker_management_actions[i+1])}")
            sel_action: str = LLlib.ask_for_digit_and_check_in_dict(worker_management_actions)

            #Execute actions
            if sel_action == "Hire workers":
                self.mainPlayer.hire_worker()
                return 0 #Energy cost
            if sel_action == "Append workers to business":
                businessList: dict[int, Business] = self.check_actions("all_businesses_player")
                sort_to_back: list = []
                print("\nSelect business")
                for i in range(len(businessList)): #index, business
                    #if b.get_worker_amount() == b.get_max_worker_amount():
                        #sort_to_back.append(b)
                    print(f"{i+1}. {businessList[i+1]}")
                targ_business: Business = LLlib.ask_for_digit_and_check_in_dict(businessList)
                if targ_business == None:
                    return 0
                else:
                    available_workers = []
                    print("Select worker")
                    for i in range(len(self.mainPlayer.workers)):
                        if not self.mainPlayer.workers[i].get_work_business():
                            available_workers.append(self.mainPlayer.workers[i])
                            print(f"{len(available_workers)}. {self.mainPlayer.workers[i]}")
                    if available_workers:
                        targ_worker: Worker = LLlib.ask_for_digit_and_check_in_dict(dict(enumerate(available_workers, 1)))
                        if targ_worker == None:
                            return 0
                        targ_business.append_to_work(targ_worker)
                        targ_worker.set_work_business(targ_business)
                        print(f"{targ_worker} now works in {targ_business}")
                        return 0
                    else:
                        print("No available workers")
                        return 0
            if sel_action == "Remove workers from business":
                businessListAll: dict[int, Business] = self.check_actions("all_businesses_player")
                businessListHasWorkers: list[Business] = []
                print("\nSelect business")
                for i in range(len(businessListAll)):
                    if businessListAll[i+1].get_worker_amount() > 0:
                        businessListHasWorkers.append(businessListAll[i+1])
                        print(f"{len(businessListHasWorkers)}. {businessListAll[i+1]}")
                targ_business = LLlib.ask_for_digit_and_check_in_dict(dict(enumerate(businessListHasWorkers, 1)))
                if targ_business == None:
                    return 0
                else:
                    print("Select worker to remove")
                    for i in range(targ_business.get_worker_amount()):
                        print(f"{i+1}. {targ_business.get_workers()[i]}")
                    targ_worker = LLlib.ask_for_digit_and_check_in_dict(dict(enumerate(targ_business.get_workers(), 1)))
                    targ_worker.remove_from_work_business()
                    targ_business.remove_from_work(targ_worker)
                    print(f"{targ_worker} has been removed from {targ_business}")
                    return 0
            
            #Tee funktioina tai if juttuina
            #Hire, append, remove
            
        
        def own_stats():
            targetEnt = self.mainPlayer
            stats_to_show = {
                "age" : targetEnt.age,
                "money" : targetEnt.get_money(),
                "owned businesses" : targetEnt.ownedBusinesses,
                "workers" : targetEnt.get_workers(),
            }
            print(f"\n\n{targetEnt.fName} {targetEnt.lName}:")
            for stat in stats_to_show:
                if not stat in ["owned businesses", "workers"]:
                    print(f"\t{stat.capitalize()}: {stats_to_show[stat]}")
                elif stat == "owned businesses":
                    print("Owned businesses:")
                    sorted_businesses = []
                    for x in stats_to_show["owned businesses"]:
                        sorted_businesses.append({"name":x.name, "business_object": x, "business_id":x.get_id()})
                    sorted_businesses.sort(key=LLlib.get_name_var_from_dict)
                    for b in sorted_businesses:
                        print(f"\t{b["name"]} ({b["business_object"].get_type()}, id:{b["business_id"]})")
                elif stat == "workers":
                    print("Workers:")
                    sorted_workers = []
                    for x in stats_to_show["workers"]:
                        x : Worker
                        sorted_workers.append({"name":str(x), "works_in":x.get_work_business().name if x.get_work_business() != None else None, "entity_id":x.get_entity_id()})
                    sorted_workers.sort(key=LLlib.get_name_var_from_dict)
                    for w in sorted_workers:
                        print(f"\t{w["name"]} ({f"Works in {w["works_in"]}" if w["works_in"] != None else "Isn't working"}, Entity id: {w["entity_id"]})")
            input("(enter anything to continue)\n->")
            return 0

        actionFunction = {
            f"{self.mainPlayer}" : own_stats,
            "Manage businesses" : manage_businesses,
            "Manage workers" : manage_workers,
        }
        if action in actionFunction:
            return actionFunction[action]()
        return 0

    def buy_Business(self, buyer, businessType):
        print(f"{buyer} is buying {businessType}")

    def create_Business(self, owner: Player|Rival, businessType, businessName):
        if businessType == LemonadeStand:
            created_business = LemonadeStand(owner=owner, name= businessName if businessName != "" else None)
        owner.ownedBusinesses.append(created_business)

entities = [Player("Eetu", "Rutanen", 15)]
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
for i in range(40):
    Game.next_day()
