import random, os

from enum import Enum, auto

os.system("")

# MENU LOGIC
class GameContoller():
    def __init__(self):
        pass
    
    @staticmethod
    def StartScreen():
        while True:
            print("=== Dark Times v1.0 ===")
            print("1. Continue")
            print("2. New Game")

            action = input("Your choice: ")

            if action == "1":
                hero = Hero(name="Auriel",
                            hp=80,
                            current_hp=80,
                            mana=50,
                            current_mana=50,
                            attack=18,
                            defend=4,
                            gold=500,
                            xp=222,
                            lvl=10
                            )
                print("Loading...")
                return hero

            elif action == "2":
                name_for_hero = input("Enter name of your hero: ")
                hero = Hero(name=name_for_hero,
                            hp=42,
                            current_hp=42,
                            mana=10,
                            current_mana=10,
                            attack=10, 
                            defend=1,
                            gold=0,
                            xp=0,
                            lvl=0)
                print("Loading...")
                return hero
    
            else:
                print("Try again.")

    @staticmethod
    def MainMenu(hero):
        # declaring merch there, otherwise invt will always reset
        merch = Merchant(gold=996)
        merch.generate_merchant_inv()

        # update hero stats, based on hero own defend and attack + gear effect boost
        hero.gear.update_hero_gear(hero)

        hero.lvl_up_sys()

        while True:
            print("=== MENU ===")
            print("1. Explore")
            print("2. Inventory")
            print("3. Shop")
            print("4. Show stats")
            print("5. Exit")

            action = input("Your choice: ")

            if action == "1":
                battle = BattleSystem()
                enemy = Enemy.enemy_factory()
                enemy.gear_based_on_enemy()
                enemy.gear.update_enemy_gear(enemy)
                battle.start_battle(hero, enemy)

            elif action == "2":
                while True:
                    print("=== Your Inventory ===")
                    hero.inventory.show(hero)

                    print("1. Use Item")
                    print("2. Equip Item")
                    print("3. Disarm Item")
                    print("4. Show Equipped Gear")
                    print("5. Leave Inventory")

                    choice = input("Your choice: ")
            
                    if choice == "1":
                        item_name = input("Enter name of item that you want to use: ")
                        hero.use(item_name)
            
                    elif choice == "2":
                        item_name = input("Enter name of item that you want to equip: ")
                        hero.equip(item_name)

                    elif choice == "3":
                        hero.gear.show_equipped()
                        item_name = input("Enter name of item that you want to disarm: ")
                        hero.dequip(item_name)

                    elif choice == "4":
                        hero.gear.show_equipped()            

                    elif choice == "5":
                        break

                    else:
                        print("Try again.")

            elif action == "3":
                while True:
                    print("=== Merchant ===")
                    print("Merchant: Greetings traveler.")
                    print("Merchant: You look tired… need potions?")

                    print("1. Buy Item(s)")
                    print("2. Sell Item(s)")
                    print("3. Rumors")
                    print("4. Leave")

                    action = input("Your choice: ")

                    if action == "1":
                        merch.show()
                        item_to_buy = input("Enter name of the item: ")
                        amount_to_buy = int(input("Enter amount that you want to buy: "))
                        merch.buy(item_to_buy, amount_to_buy, hero)

                    elif action == "2":
                        hero.inventory.show()
                        item_to_sell = input("Enter name of the item: ")
                        amount_to_sell = int(input("Enter amount that you want to sell: "))
                        merch.sell(item_to_sell, amount_to_sell, hero)

                    elif action == "3":
                        merch.rumors()

                    elif action == "4":
                        break

                    else:
                        print("Try Again.")

            elif action == "4":
                hero.show_stats()

            elif action == "5":
                break

            else:
                print("Try again.")

# EXPLORE SYS, BATTLE LOGIC
class BattleSystem:
    def __init__(self):
        self.battle_action = BattleAction()

    def start_battle(self, hero, enemy):
        print("A wild", enemy.name.lower(), "appears!")
        while hero.is_alive() and enemy.is_alive():
            
            hero_mh = False
            hero_att = hero.attack
            hero_defe = hero.defend

            enemy_mh = False
            enemy_att = enemy.attack
            enemy_defe = enemy.defend
            
            hero.health_bar.draw()
            enemy.health_bar.draw()

            print("1. Attack")
            print("2. Magic")
            print("3. Run")

            action = input("Your choice: ")

            tried_to_escape = False

            if action == "1":
                # hero battle logic
                weapon_type = self.battle_action.get_weapon_type(hero)
                self.battle_action.attack_types(weapon_type)
            

                hero_choice = self.battle_action.choice()

                mh, att, defe, move = self.battle_action.character_attack_choice(weapon_type, hero, hero_choice)

                hero_mh = mh
                hero_att = int(att)
                hero_defe = int(defe)
                hero_move = move

                hero_att = self.battle_action.crit(hero_att)

                # enemy battle logic
                weapon_type = self.battle_action.get_weapon_type(enemy)

                enemy_choice = str(random.randint(1, 4))

                mh, att, defe, move = self.battle_action.character_attack_choice(weapon_type, enemy, enemy_choice)
                
                enemy_mh = mh
                enemy_att = int(att)
                enemy_defe = int(defe)
                enemy_move = move

                enemy_att = self.battle_action.crit(enemy_att)

                 # gets miss_or_hit, prints messages
                if hero_mh == False:
                    self.battle_action.attack_move(enemy, hero_att, enemy_defe)
                    hero.health_bar.update()
                    print(f"Using move '{hero_move}' you deal {self.battle_action.hero_dmg(hero_att, enemy_defe)} damage by using {self.battle_action.get_weapon(hero)}!")
                else:
                    print("You missed!")

                if enemy_mh == False:
                    self.battle_action.attack_move(hero, enemy_att, hero_defe)
                    enemy.health_bar.update()
                    print(f"Using move '{enemy_move}' enemy deals {self.battle_action.enemy_dmg(enemy_att, hero_defe)} damage by using {self.battle_action.get_weapon(enemy)}!")
                else:
                    print("Enemy missed!")

            elif action == "2":
                scr_name, scr_type, scr_eff, mana_cost = self.battle_action.get_scrolls(hero)
                hero.current_mana -= mana_cost

                if scr_type == "Healing":
                    hero.current_hp += scr_eff
                    if hero.current_hp > hero.hp:
                        hero.current_hp = hero.hp
                    print(f"Using '{scr_name}' you heal {scr_eff} HP!")

                elif scr_type == "Destruction":
                    # there could be like magical character defend, like POE2 where your defense type matters
                    self.battle_action.attack_move(enemy, scr_eff, enemy_defe)
                    print(f"Using '{scr_name}' you deal {scr_eff} magical DMG!")
                
                # YEAH, DONT REPEAT YOURSELF, but for now thats faster
                # enemy battle logic
                weapon_type = self.battle_action.get_weapon_type(enemy)

                enemy_choice = str(random.randint(1, 4))

                mh, att, defe, move = self.battle_action.character_attack_choice(weapon_type, enemy, enemy_choice)
                
                enemy_mh = mh
                enemy_att = int(att)
                enemy_defe = int(defe)
                enemy_move = move

                enemy_att = self.battle_action.crit(enemy_att)

                if enemy_mh == False:
                    self.battle_action.attack_move(hero, enemy_att, hero_defe)
                    enemy.health_bar.update()
                    print(f"Using move '{enemy_move}' enemy deals {self.battle_action.enemy_dmg(enemy_att, hero_defe)} damage by using {self.battle_action.get_weapon(enemy)}!")
                else:
                    print("Enemy missed!")
                
            elif action == "3":
                stay_or_escape = random.randint(1, 2)
                tried_to_escape = True
                if stay_or_escape == 1:
                    break

                else:
                    print("You failed to escape.")
                    # enemy battle logic
                    weapon_type = self.battle_action.get_weapon_type(enemy)

                    enemy_choice = str(random.randint(1, 4))

                    mh, att, defe, move = self.battle_action.character_attack_choice(weapon_type, enemy, enemy_choice)
                
                    enemy_mh = mh
                    enemy_att = int(att)
                    enemy_defe = int(defe)
                    enemy_move = move

                    enemy_att = self.battle_action.crit(enemy_att)
                    
                    hero.health_bar.update()

                    print(f"Using move '{enemy_move}' enemy deals {self.battle_action.enemy_dmg(enemy_att, hero_defe)} damage by using {self.battle_action.get_weapon(enemy)}!")

            else:
                print("Try again.")

        if not hero.is_alive():
            print("YOU DIED")
            start = GameContoller.StartScreen()
            menu = GameContoller.MainMenu(start)
            

        else:
            if tried_to_escape == False:
                print("Enemy have been defeated.")
                hero.xp += enemy.xp
                print("You gained ", enemy.xp, "XP.")
                hero.gold += enemy.gold
                print("You found ", enemy.gold, "gold.")
                self.battle_action.loot(hero, enemy, weapon_type)
                item = Item.random_item()
                print(f"Additionally you found: {item.name}")
                hero.inventory.add(item)
                return

            else:
                print("You escaped.")
        
class BattleAction():
    def __init__(self):
        pass

    def percentage(self, part, whole):
        return int((part * whole) / 100)
    
    def choice(self):
            while True:
                choice = input("Your choice: ")
                if choice == "1" or choice == "2" or choice == "3" or choice == "4":
                    return choice
                else:
                    print("Try again.")

    def attack_move(self, target, attack, defend):
        damage = attack - defend
        if damage < 0:
            damage = 0
        target.take_damage(damage)

    def hero_dmg(self, hero_att, enemy_defe):
        if hero_att - enemy_defe < 0:
            return 0
        else:
            return hero_att - enemy_defe
        
    def enemy_dmg(self, enemy_att, hero_defe):
        if enemy_att - hero_defe < 0:
            return 0
        else:
            return enemy_att - hero_defe
    
    def get_weapon(self, character):
        if character.gear.hands != None:
            return character.gear.hands.name
        elif character.gear.right_hand != None and isinstance(character.gear.left_hand, Weapon):
            return (f"{character.gear.right_hand.name} and {character.gear.left_hand.name}")
        elif character.gear.right_hand != None and isinstance(character.gear.left_hand, Armour):
            return character.gear.right_hand.name
        elif character.gear.right_hand != None or isinstance(character.gear.left_hand, Weapon):
            return (character.gear.right_hand.name if character.gear.right_hand else character.gear.left_hand)
        else:
            return fists.name

    def get_weapon_type(self, character):
        if character.gear.hands != None and character.gear.hands.weapon_type == "Sharp":
            return "two-handed"
        if character.gear.hands != None and character.gear.hands.weapon_type == "Pierce":
            return "heavy polearm"
        elif character.gear.right_hand != None and isinstance(character.gear.left_hand, Weapon):
            return "dual-wield"
        elif character.gear.right_hand != None and isinstance(character.gear.left_hand, Armour):
            return "one-handed and shield"
        elif character.gear.right_hand != None or isinstance(character.gear.left_hand, Weapon):
            return 'one-handed'
        else:
            return 'disarmed'

    def attack_types(self, weapon_type):
        if weapon_type == "two-handed":
            print(f"1. Regular attack === regular damage, 25% chance to miss")
            print(f"2. Quick Slash === 80% damage but guaranteed hit")
            print(f"3. Heavy Strike === double damage, 50% chance to miss")
            print(f"4. Guard === +40% defense for 1 turn")
        elif weapon_type == "heavy polearm":
            print(f"1. Regular attack === regular damage, 20% chance to miss")
            print(f"2. Sure Pierce === 75% damage but guaranteed hit")
            print(f"3. Macedonian Technique === double damage, 40% chance to miss")
            print(f"4. Keep Distance === +35% defense for 1 turn")
        elif weapon_type == "dual-wield":
            print(f"1. Regular attack === regular damage, 30% chance to miss")
            print(f"2. Defensive Slash === 80% damage but guaranteed hit")
            print(f"3. Double Strike === double damage, 50% chance to miss")
            print(f"4. Guard === +30% defense for 1 turn")
        elif weapon_type == "one-handed and shield":
            print(f"1. Regular attack === regular damage, 25% chance to miss")
            print(f"2. Under Attack === 75% damage but guaranteed hit")
            print(f"3. Faint === +50% damage, +35% defense, 45% chance to miss")
            print(f"4. Guard === +80% defense for 1 turn")
        elif weapon_type == "one-handed":
            print(f"1. Regular attack === regular damage, 20% chance to miss")
            print(f"2. Commander's Attack === 80% damage but guaranteed hit")
            print(f"3. Lorraine's Technique === +50% damage, +10% defense, 50% chance to miss")
            print(f"4. Parry === +45% defense for 1 turn")
        elif weapon_type == "disarmed":
            print(f"1. Regular attack === regular damage, 20% chance to miss")
            print(f"2. Counter Punch === 80% damage but guaranteed hit")
            print(f"3. Powerful Punch === +60% damage, 40% chance to miss")
            print(f"4. Evasion === +25% defense for 1 turn")

    def character_attack_choice(self, weapon_type, character, choice):
        miss_or_hit = random.randint(1, 21)
        attack = character.attack
        defend = character.defend
        # two-handed
        if weapon_type == "two-handed":
            # reutrn miss_hit, attack, defense, att move
            if choice == "1":
                if miss_or_hit <= 15:
                    return False, attack, defend, "Regular attack"
                else:
                    return True, 0, defend, "Regular attack"
            elif choice == "2":
                return False, self.percentage(80, attack), defend, "Quick Slash"
            elif choice == "3":
                if miss_or_hit >= 10:
                    return False, self.percentage(200, attack), defend, "Heavy Strike"
                else:   
                    return True, 0, defend, "Heavy Strike"
            elif choice == "4":
                return False, 0, self.percentage(140, defend), "Guard"
        # heavy polearm
        elif weapon_type == "heavy polearm":
            if choice == "1":
                if miss_or_hit <= 16:
                    return False, attack, defend, "Regular attack"
                else:
                    return True, 0, defend, "Regular attack"
            elif choice == "2":
                return False, self.percentage(75, attack), defend, "Sure Pierce"
            elif choice == "3":
                if miss_or_hit >= 12:
                    return False, self.percentage(200, attack), defend, "Macedonian Technique"
                else:   
                    return True, 0, defend, "Macedonian Technique"
            elif choice == "4":
                return False, 0, self.percentage(135, defend), "Keep Distance"
        # dual-wield
        elif weapon_type == "dual-wield":
            if choice == "1":
                if miss_or_hit <= 14:
                    return False, attack, defend, "Regular attack"
                else:
                    return True, 0, defend, "Regular attack"
            elif choice == "2":
                return False, self.percentage(80, attack), defend, "Defensive Slash"
            elif choice == "3":
                if miss_or_hit >= 10:
                    return False, self.percentage(200, attack), defend, "Double Strike"
                else:   
                    return True, 0, defend, "Double Strike"
            elif choice == "4":
                return False, 0, self.percentage(130, defend), "Guard"
        # one-handed and shield
        elif weapon_type == "one-handed and shield":
            if choice == "1":
                if miss_or_hit <= 15:
                    return False, attack, defend, "Regular attack"
                else:
                    return True, 0, defend, "Regular attack"
            elif choice == "2":
                return False, self.percentage(75, attack), defend, "Under Attack"
            elif choice == "3":
                if miss_or_hit >= 11:
                    return False, self.percentage(150, attack), self.percentage(135, defend), "Faint"
                else:   
                    return True, 0, defend, "Faint"
            elif choice == "4":
                return False, 0, self.percentage(180, defend), "Guard"
        # one-handed
        elif weapon_type == "one-handed":
            if choice == "1":
                if miss_or_hit <= 16:
                    return False, attack, defend, "Regular attack"
                else:
                    return True, 0, defend, "Regular attack"
            elif choice == "2":
                return False, self.percentage(80, attack), defend, "Commander's Attack"
            elif choice == "3":
                if miss_or_hit >= 10:
                    return False, self.percentage(150, attack), self.percentage(110, defend), "Lorraine's Technique"
                else:   
                    return True, 0, defend, "Lorraine's Technique"
            elif choice == "4":
                return False, 0, self.percentage(145, defend), "Parry"
        # disarmed
        elif weapon_type == "disarmed":
            # reutrn miss_hit, attack, defense, att move
            if choice == "1":
                if miss_or_hit <= 15:
                    return False, attack, defend, "Regular attack"
                else:
                    return True, 0, defend, "Regular attack"
            elif choice == "2":
                return False, self.percentage(80, attack), defend, "Counter Punch"
            elif choice == "3":
                if miss_or_hit >= 12:
                    return False, self.percentage(160, attack), defend, "Powerful Punch"
                else:   
                    return True, 0, defend, "Powerful Punch"
            elif choice == "4":
                return False, 0, self.percentage(125, defend), "Evasion"

    # doubles dmg, chance 1/6    
    def crit(self, attack):
        crit_random = random.randint(1, 6)
        if crit_random == 1:
            return self.percentage(200, attack)
        else:
            return attack
    
    # loot sys for hero, random gear of class armour and weapon
    def loot(self, hero, enemy, weapon_type):
        armour_num = random.randint(1, 6)
        if armour_num == 1:
            if enemy.gear.head != None:
                print(f"You found: {enemy.gear.head.name}!")
                hero.inventory.add(enemy.gear.head)
        elif armour_num == 2:
            if enemy.gear.chest != None:
                print(f"You found: {enemy.gear.chest.name}!")
                hero.inventory.add(enemy.gear.chest)
        elif armour_num == 3:
            if enemy.gear.pants != None:
                print(f"You found: {enemy.gear.pants.name}!")
                hero.inventory.add(enemy.gear.pants)
        elif armour_num == 4:
            if enemy.gear.boots != None:
                print(f"You found: {enemy.gear.boots.name}!")
                hero.inventory.add(enemy.gear.boots)
        elif armour_num == 5:
            if enemy.gear.gauntlets != None:
                print(f"You found: {enemy.gear.gloves.name}!")
                hero.inventory.add(enemy.gear.gloves)
        elif armour_num == 6:
            if enemy.gear.left_hand != None and isinstance(enemy.gear.left_hand, Armour):
                print(f"You found: {enemy.gear.left_hand.name}!")
                hero.inventory.add(enemy.gear.left_hand)

        weapon_num = random.randint(1, 4)
        if weapon_num == 1:
            if weapon_type == "two-handed" or weapon_type == "heavy polearm":
                print(f"You found: {enemy.gear.hands.name}!")
                hero.inventory.add(enemy.gear.hands)
        elif weapon_num == 2:
            if weapon_type == "dual-wield":
                print(f"You found: {enemy.gear.right_hand.name} and {enemy.gear.left_hand.name}!")
                hero.inventory.add(enemy.gear.right_hand)
                hero.inventory.add(enemy.gear.left_hand)
        elif weapon_num == 3:
            if weapon_type == "one-handed and shield":
                print(f"You found: {enemy.gear.right_hand.name} and {enemy.gear.left_hand.name}!")
                hero.inventory.add(enemy.gear.right_hand)
                hero.inventory.add(enemy.gear.left_hand)
        elif weapon_num == 4:
            if weapon_type == "one-handed":
                if enemy.gear.left_hand != None:
                    print(f"You found: {enemy.gear.left_hand.name}!")
                    hero.inventory.add(enemy.gear.left_hand)
                else:
                    print(f"You found: {enemy.gear.right_hand.name}!")
                    hero.inventory.add(enemy.gear.right_hand)

    def get_scrolls(self, character):
        print("=== Your Scrolls ===")
        battle_inv = {}
        for name, data in character.inventory.items.items():
            if isinstance(data["item"], Scroll):
                item_obj = data["item"]

                battle_inv[item_obj.name] = {"item": item_obj, "scroll_type": item_obj.scroll_type, "effect": item_obj.effect, "amount": data["amount"]}
            
        for name, data in battle_inv.items():
            print(f"{name} | Type: {data["scroll_type"]} | Effect: {data["effect"]} | Amount: {data["amount"]}")

        while True:
            print("Do you want to use scroll?")
            action = input("Yes(Y) or No(N): ")

            if action == "Y":
                scroll_name = input("Enter name of the scroll: ")
                if scroll_name not in battle_inv:
                    print("No such item.")

                else:
                    # reutrn name of the scroll, effect, cost of mana
                    item_obj = battle_inv[scroll_name]["item"]
                    character.inventory.remove(item_obj.name, 1)
                    return item_obj.name, item_obj.scroll_type, int(item_obj.effect), int(item_obj.effect / 5)

            elif action == "N":
                break

            else:
                print("Try again.")
            

class HealthBar:
    symbol_remaining: str = "█"
    symbol_lost: str = "_"
    barrier: str = "|"
    colors: dict = {
        "red": "\033[91m",
        "blue": "\33[34m",
        "green": "\033[92m",
        "yellow": "\33[93m",
        "grey": "\33[37m",
        "default": "\033[0m"
    }

    def __init__(self, entity, length: int = 20, is_colored: bool = True, color: str = ""):
        self.entity = entity
        self.length = length
        self.max_value = entity.hp
        self.current_value = entity.current_hp

        self.is_colored = is_colored
        self.color = self.colors.get(color) or self.colors["default"]

    def update(self):
        self.current_value = self.entity.current_hp

    def draw(self):
        remaining_bars = round(self.current_value / self.max_value * self.length)
        lost_bars = self.length - remaining_bars
        print(f"{self.entity.name}'s HEALTH: {self.entity.current_hp}/{self.entity.hp}")
        print(f"{self.barrier}"
              f"{self.color if self.is_colored else ''}"
              f"{remaining_bars * self.symbol_remaining}"
              f"{lost_bars * self.symbol_lost}"
              f"{self.colors["default"] if self.is_colored else ''}"
              f"{self.barrier}")

# CHARACTER, HERO, ENEMY
class Character:
    def __init__(self, name, hp, current_hp, mana, current_mana, attack, defend, gold, xp):
        self.name = name
        self.hp = hp
        self.current_hp = current_hp
        self.mana = mana
        self.current_mana = current_mana
        self.attack = attack
        self.defend = defend
        self.gold = gold
        self.xp = xp

    def take_damage(self, amount):
        self.current_hp -= amount

    def is_alive(self):
        if self.current_hp <= 0:
            return False
        else:
            return True

class Hero(Character):
    def __init__(self, name, hp, current_hp, mana, current_mana, attack, defend, gold, xp, lvl):
        super(). __init__(name, hp, current_hp, mana, current_mana, attack, defend, gold, xp)
        self.inventory = Inventory()
        self.gear = Gear()
        self.lvl = lvl

        self.health_bar = HealthBar(self, color="green")

    def use(self, item_name):
        if item_name not in self.inventory.items:
            print("You don't have that item!")
            return
        
        item_obj = self.inventory.items[item_name]["item"]

        if isinstance(item_obj, Weapon) or isinstance(item_obj, Armour):
            print("This item cannot be used.")
            return

        if item_name == "HP Potion":
            self.current_hp += item_obj.effect
            if self.current_hp > self.hp:
                self.current_hp = self.hp

        else:
            self.mana += item_obj.effect
            if self.current_mana > self.mana:
                self.current_hp = self.mana

        print(f"{self.name} used {item_name}!")
        self.inventory.items[item_name]["amount"] -= 1

        if self.inventory.items[item_name]["amount"] == 0:
            del self.inventory.items[item_name]

    def equip(self, item_name):
        if item_name not in self.inventory.items:
            print("You don't have this item.")
            return

        item_obj = self.inventory.items[item_name]["item"]

        # ---- WEAPONS ----
        if isinstance(item_obj, Weapon):
            if item_obj == self.gear.right_hand and item_obj == self.gear.left_hand:
                print("You already have this as equipped in both hands.")
                return
            # two-handed: right and left hand are occupied
            elif item_obj.weapon_size == "Heavy":
                self.gear.hands = item_obj
                if self.gear.right_hand != None and self.gear.left_hand != None:
                    self.inventory.add(self.gear.right_hand)
                    self.inventory.add(self.gear.left_hand)
                elif self.gear.right_hand != None:
                    self.inventory.add(self.gear.right_hand)
                elif self.gear.left_hand != None:
                    self.inventory.add(self.gear.left_hand)
                else:
                    pass
 
                self.gear.right_hand = None
                self.gear.left_hand = None

            # two-handed: hero already has weapon_type heavy equipped
            elif self.gear.hands != None:
                self.inventory.add(self.gear.hands)
                self.gear.hands = None
                self.gear.right_hand = item_obj

            # both hands have same weapon, user should choose in which hand swap weapon
            elif isinstance(self.gear.right_hand, Weapon) and isinstance(self.gear.left_hand, Weapon):
                while True:
                    print("In which hand you want to change weapon?")

                    choice = input("Right hand(Right) or left hand(left): ")
                    if choice == "Right":
                        self.inventory.add(self.gear.right_hand)
                        self.gear.right_hand = item_obj
                        break

                    elif choice == "Left":
                        self.inventory.add(self.gear.left_hand)
                        self.gear.left_hand = item_obj
                        break
                
                    else:
                        print("Try again.")

            # one-handed: right is empty, left has sword
            elif self.gear.right_hand == None and isinstance (self.gear.left_hand, Weapon):
                self.gear.left_hand = item_obj

            # one-handed: right hand is empty, left has shield
            elif self.gear.right_hand == None and isinstance (self.gear.left_hand, Armour):
                self.gear.left_hand = item_obj

            # one-handed: right ocuppied, left has weapon
            elif self.gear.right_hand != None:
                self.gear.left_hand = item_obj
            
            else:
                # one-handed: both hands are empty, right hand first
                self.gear.right_hand = item_obj

        # ---- ARMOUR ----
        elif isinstance(item_obj, Armour):
            match item_obj.armour_type:
                case "Helmet":
                    if self.gear.head != None:
                        self.inventory.add(self.gear.head)
                        self.gear.head = None
                    self.gear.head = item_obj
                case "Breastplate":
                    if self.gear.chest != None:
                        self.inventory.add(self.gear.chest)
                        self.gear.chest = None
                    self.gear.chest = item_obj
                case "Gauntlets":
                    if self.gear.gauntlets != None:
                        self.inventory.add(self.gear.gauntlets)
                        self.gear.gauntlets = None
                    self.gear.gauntlets = item_obj
                case "Shield":
                    if self.gear.left_hand != None:
                        self.inventory.add(self.gear.left_hand)
                        self.gear.left_hand = None
                    self.gear.left_hand = item_obj
                case "Pants":
                    if self.gear.pants != None:
                        self.inventory.add(self.gear.pants)
                        self.gear.pants = None
                    self.gear.pants = item_obj
                case "Boots":
                    if self.gear.boots != None:
                        self.inventory.add(self.gear.boots)
                        self.gear.boots = None
                    self.gear.boots = item_obj
    
        else:
            print("You can't equip this.")
            return
    
        # remove from inventory
        self.inventory.remove(item_name, 1)
        print(f"{self.name} equipped {item_name}!")


    def dequip(self, slot):
        if getattr(self.gear, slot) is None:
            print("Nothing equipped there.")
            return
    
        item = getattr(self.gear, slot)
        print (item.name)
        self.inventory.add(item)
        setattr(self.gear, slot, None)

        # if weapon removed, restore fists
        if isinstance(item, Weapon):
            self.right_hand = fists
            self.left_hand = fists
    
        print(f"{item.name} removed.")
    
    # lvl sys, with lvl barriers and increasing hp, mana and attack when hero lvls up
    def lvl_up_sys(self):
        level_barrier = [0, 10, 50, 100, 300, 500, 1000, 1800]
        lvl = len([s for s in level_barrier if self.xp > s])
        self.lvl = lvl
        if self.lvl > 0:
            self.attack += int(lvl * 1.3)
            self.hp += int(lvl * 1.6)
            self.mana += int(lvl * 1.2)
        else:
            pass
            

    def show_stats(self):
        print("Name:", self.name, "| HP:", self.hp, "| Attack:", self.attack, "| Defense:", int(self.defend), "| XP:", self.xp)

class Enemy(Character):
    def __init__(self, name, hp, current_hp, mana, current_mana, attack, defend, gold, xp):
        super().__init__(name, hp, current_hp, mana, current_mana, attack, defend, gold, xp)
        self.gear = Gear()
        
        self.health_bar = HealthBar(self, color="red")

    def enemy_factory():
        orc = Enemy(name="Orc",
                    hp=50,
                    current_hp=50,
                    mana= 10,
                    current_mana=10,
                    attack=4,
                    defend=3,
                    gold=5,
                    xp=10
                    )
        goblin = Enemy(name="Goblin",
                       hp=35,
                       current_hp=35,
                       mana=20,
                       current_mana=20,
                       attack=2,
                       defend=2,
                       gold=3,
                       xp=8
                       )
        undead = Enemy(name="Undead",
                       hp=80,
                       current_hp=80,
                       mana=5,
                       current_mana=5,
                       attack=3,
                       defend=4,
                       gold=2,
                       xp=12
                       )
        enemies = [orc, goblin, undead]
        return random.choice(enemies)
    
    def gear_based_on_enemy(self):
        num = random.randint(1, 4)
        if self.name == "Orc":
            self.gear.head = knight_helmet
            self.gear.chest = leather_armour
            self.gear.pants = mail_chausses
            self.gear.boots = riding_boots

            def orc_weapon(variation):
                if variation == 1:
                    self.gear.right_hand = iron_sword
                elif variation == 2:
                    self.gear.right_hand = iron_mace
                    self.gear.left_hand = shadow_shield
                elif variation == 3:
                    self.gear.hands = zweihander
                elif variation == 4:
                    self.gear.right_hand = iron_sword
                    self.gear.left_hand = iron_sword

            orc_weapon(num)
        
        elif self.name == "Goblin":
            self.gear.head = mercenary_bascinet
            self.gear.chest = leather_armour
            self.gear.gauntlets = hunter_gloves
            self.gear.boots = riding_boots

            def goblin_weapon(variation):
                if variation == 1:
                    self.gear.right_hand = iron_sword
                elif variation == 2:
                    self.gear.right_hand = iron_mace
                    self.gear.left_hand = shadow_shield
                elif variation == 3:
                    self.gear.hands = iron_spear
                elif variation == 4:
                    self.gear.right_hand = iron_sword
                    self.gear.left_hand = iron_sword

            goblin_weapon(num)

        elif self.name == "Undead":
            self.gear.chest = leather_armour
            self.gear.pants = green_hose
            self.gear.boots = riding_boots

            self.gear.right_hand = undead_fists
            self.gear.left_hand = undead_fists


# ITEMS, WEAPONS, SCROLLS, ARMORS
class Item:
    def __init__(self, name, effect, price, tradeable:bool):
        self.name = name
        self.effect = effect
        self.price = price
        self.tradeable = tradeable

    def random_item():
        item = random.choice([hp_potion, mana_potion])
        return item

class Weapon(Item):
    def __init__(self, name, effect, price, weapon_type, weapon_size, tradeable):
        super(). __init__(name, effect, price, tradeable)  
        self.weapon_type = weapon_type
        self.weapon_size = weapon_size

class WeaponType(Enum):
    SHARP = auto()
    BLUNT = auto()
    PIERCE = auto()

class WeaponSize(Enum):
    LIGHT = auto()
    MEDIUM = auto()
    HEAVY = auto()

class Scroll(Item):
    def __init__(self, name, effect, price, scroll_type, tradeable):
        super(). __init__(name, effect, price, tradeable)
        self.scroll_type = scroll_type

class ScrollType(Enum):
    DESTRUCTION = auto()
    HEALING = auto()

class Armour(Item):
    def __init__(self, name, effect, price, armour_type, armour_size, tradeable):
        super(). __init__(name, effect, price, tradeable)
        self.armour_type = armour_type
        self.armour_size = armour_size

class ArmourType(Enum):
    HELMET = auto()
    BREASTPLATE = auto()
    GAUNTLETS = auto()
    SHIELD = auto()
    LEGS = auto()
    BOOTS = auto()
    RING = auto()
    AMULET = auto()

class ArmourSize(Enum):
    LIGHT = auto()
    MEDIUM = auto()
    HEAVY = auto()


class Inventory:
    def __init__(self):
        self.items = {zweihander.name:{"item": zweihander, "amount": 2}, 
                    scroll_of_fire_ball.name:{"item": scroll_of_fire_ball, "amount": 4},
                    scroll_of_healing_school.name:{"item": scroll_of_healing_school, "amount": 3}}

    def add(self, item_obj, amount=1):
        name = item_obj.name

        if item_obj.tradeable == False:
            return
        
        else:
            if name not in self.items:
                self.items[name] = {"item": item_obj, "amount": amount}
            else:
                self.items[name]["amount"] += amount

    def remove(self, item_name, amount):
        self.items[item_name]["amount"] -= amount
        if self.items[item_name]["amount"] == 0:
            del self.items[item_name]

    def show(self, hero):
        print(f"{hero.gold} GOLD")
        for name, data in self.items.items():
            print(f"{name} x{data["amount"]}")

class Gear:
    def __init__(self):
        self.head = None
        self.chest = None
        self.gauntlets = None
        self.hands = None
        self.right_hand = None
        self.left_hand = None
        self.pants = None
        self.boots = None

    def show_equipped(self):
        print("=== Gear ===")
        print("Helmet:", self.head.name if self.head else "None")
        print("Chest:", self.chest.name if self.chest else "None")
        print("Gauntlets:", self.gauntlets.name if self.gauntlets else "None")
        print("Both Hands:", self.hands.name if self.hands else "None")
        print("Right hand:", self.right_hand.name if self.right_hand else "None")
        print("Left hand:", self.left_hand.name if self.left_hand else "None")
        print("Pants:", self.pants.name if self.pants else "None")
        print("Boots:", self.boots.name if self.boots else "None")

    def update_hero_gear(self, hero):
        # defense
        gear_defend = 0
        if self.head != None:
            gear_defend += self.head.effect

        if self.chest != None:
            gear_defend  += self.chest.effect
        
        if self.gauntlets != None:
            gear_defend += self.gauntlets.effect

        if isinstance(self.left_hand, Armour):
            gear_defend += self.left_hand.effect

        if self.pants != None:
            gear_defend += self.pants.effect

        if self.boots != None:
            gear_defend += self.boots.effect

        hero.defend += gear_defend / 2

        # attack
        gear_attack = 0
        if self.right_hand != None:
            gear_attack += self.right_hand.effect

        if self.left_hand != None and isinstance(self.left_hand, Weapon):
            gear_attack += self.right_hand.effect

        elif self.hands != None:
            gear_attack += self.hands.effect

        hero.attack += gear_attack

    def update_enemy_gear(self, enemy):
        # defense
        gear_defend = 0
        if self.head != None:
            gear_defend += self.head.effect

        if self.chest != None:
            gear_defend  += self.chest.effect

        if self.gauntlets != None:
            gear_defend += self.gauntlets.effect

        if isinstance(self.left_hand, Armour):
            gear_defend += self.left_hand.effect

        if self.pants != None:
            gear_defend += self.pants.effect

        if self.boots != None:
            gear_defend += self.boots.effect

        enemy.defend += gear_defend /2

        # attack
        gear_attack = 0
        if self.right_hand != None:
            gear_attack += self.right_hand.effect

        if self.left_hand != None and isinstance(self.left_hand, Weapon):
            gear_attack += self.right_hand.effect

        elif self.hands != None:
            gear_attack += self.hands.effect

        enemy.attack += gear_attack
        

# MERHCANT -> BUY AND SELL LOGIC
class Merchant:
    def __init__(self, gold):
        self.gold = gold
        self.merch_inventory = {}
    
    def generate_merchant_inv(self):
        self.merch_inventory[hp_potion.name] = {"item": hp_potion, "effect": hp_potion.effect, "price": hp_potion.price, "amount": 22}
        self.merch_inventory[mana_potion.name] = {"item": mana_potion, "effect": hp_potion.effect, "price": mana_potion.price, "amount": 13}
        self.merch_inventory[mail_chausses.name] = {"item": mail_chausses, "effect": mail_chausses.effect, "type": mail_chausses.armour_type, "price": mail_chausses.price, "amount": 3}
        self.merch_inventory[iron_mace.name] = {"item": iron_mace, "effect": iron_mace.effect, "type": iron_mace.weapon_type, "price": iron_mace.price, "amount": 4}
        self.merch_inventory[iron_sword.name] = {"item": iron_sword, "effect": iron_sword.effect, "type": iron_sword.weapon_type, "price": iron_sword.price, "amount": 7}
        self.merch_inventory[leather_armour.name] = {"item": leather_armour, "effect": leather_armour.effect, "type": leather_armour.armour_type, "price": leather_armour.price, "amount": 4}
        self.merch_inventory[knight_helmet.name] = {"item": knight_helmet, "effect": knight_helmet.effect, "type": knight_helmet.armour_type, "price": knight_helmet.price, "amount": 4}
        self.merch_inventory[hunter_gloves.name] = {"item": hunter_gloves, "effect": hunter_gloves.effect, "type": hunter_gloves.armour_type, "price": hunter_gloves.price, "amount": 2}
        self.merch_inventory[zweihander.name] = {"item": zweihander, "effect": zweihander.effect, "type": zweihander.weapon_type, "price": zweihander.price, "amount": 2}


    def show(self):
        for name, data in self.merch_inventory.items():
                if isinstance (self.merch_inventory[name]["item"], Weapon):
                    print(f"WEAPON: {name} | Effect: {data["effect"]} DMG | Weapon Type: {data["type"]} | Price: {data["price"]} GOLD | Amount: x{data["amount"]}")
                
                elif isinstance (self.merch_inventory[name]["item"], Armour):
                    print(f"ARMOUR: {name} | Effect: {data["effect"]} DEF | Armour Type: {data["type"]} | Price: {data["price"]} GOLD | Amount: x{data["amount"]}")
                
                elif not isinstance (self.merch_inventory[name]["item"], Armour and Weapon):
                    print(f"UTILITY: {name} | Effect: {data["effect"]} HP/MANA | Price: {data["price"]} GOLD | Amount: x{data["amount"]}")
    
    def remove_item(self, item_name, amount):
        self.merch_inventory[item_name]["amount"] -= amount
        if self.merch_inventory[item_name]["amount"] <= 0:
            del self.merch_inventory[item_name]
    
    def buy(self, item_name, amount, hero):
        if not item_name in self.merch_inventory:
            print("Merchant don't have this item.")
            return
        
        if amount > self.merch_inventory[item_name]["amount"]:
            print("Merchant don't have enough amount.")
            return

        item_obj = self.merch_inventory[item_name]["item"]

        total_price = item_obj.price * amount
        total_price = int(total_price)

        while True:
            print(f"You will buy: {item_name} | Amount: {amount} | Total price: {total_price}")
            print(f"Your balance is: {hero.gold}")
            print("Are you sure?")
            answer = input("Yes(Y) or No(N): ")

            if answer == "Y":
                hero.gold -= total_price
                self.gold += total_price
                hero.inventory.add(item_obj, amount)
                self.remove_item(item_name, amount)
                print("Purchase was succesfull.")
                break

            elif answer == "N":
                break

            else:
                print("Try again.")

    def sell(self, item_name, amount, hero):
        if not item_name in hero.inventory.items:
            print("You don't have this item.")
            return
        
        if amount > hero.inventory.items[item_name]["amount"]:
            print("You don't have enough amount.")
            return
        
        item_obj = hero.inventory.items[item_name]["item"]

        total_price = (item_obj.price * amount) / 3
        total_price = int(total_price)

        if total_price > self.gold:
            print(f"Merchant has only: {self.gold} GOLD, but total price: {total_price} GOLD.")
            return
        
        while True:
            print(f"You will sell: {item_name} | Amount: {amount} | Total price: {total_price}")
            print("Are you sure?")
            answer = input("Yes(Y) or No(N): ")

            if answer == "Y":
                hero.gold += total_price
                self.gold -= total_price

                hero.inventory.remove(item_name, amount)
                self.add(item_name, amount, hero)

                print("Deal was succesfull.")
                break

            elif answer == "N":
                break

            else:
                print("Try again.")
        
    def add(self, item_name, amount, hero):
        if not item_name in self.merch_inventory:
            item_obj = hero.inventory.items[item_name]["item"]
            if not isinstance (item_obj, Weapon):
                self.merch_inventory[item_name] = {"item": item_obj, "effect": item_obj.effect, "price": item_obj.price, "amount": amount}

            elif isinstance (item_obj, Weapon):
                self.merch_inventory[item_name] = {"item": item_obj, "effect": item_obj.effect, "type": item_obj.weapon_type, "price": item_obj.price, "amount": amount}

        else:
            self.merch_inventory[item_name]["amount"] += amount

    def rumors(self):
        phrases = ["Have you seen castle of Zimburg? It's magnificent.", 
                   "Better don't go to the woods in the night. Someone screams there", 
                   "There is rumor that in a caves of Rocktown our count hides his gold."]
        random_phrase = random.choice(phrases)
        print(random_phrase)

# Objects of ITEMS
hp_potion = Item(name="HP Potion",
                 effect=10,
                 price=10,
                 tradeable=True
                 )

mana_potion = Item(name="Mana Potion",
                   effect=10,
                   price=12,
                   tradeable=True
                   )

# Objects of SCROLLS
scroll_of_fire_ball = Scroll(name="Scroll of Fire Ball",
                             effect=20,
                             price=110,
                             scroll_type=ScrollType.DESTRUCTION,
                             tradeable=True)

scroll_of_healing_school = Scroll(name="Scroll of Healing School",
                             effect=15,
                             price=100,
                             scroll_type=ScrollType.HEALING,
                             tradeable=True)

# Objects of WEAPONS
iron_spear = Weapon(name="Iron Spear",
                    effect=13,
                    price=122,
                    weapon_type=WeaponType.PIERCE,
                    weapon_size=WeaponSize.HEAVY,
                    tradeable=True
                    )

zweihander = Weapon(name="Zweihander",
                    effect=16,
                    price=142,
                    weapon_type=WeaponType.SHARP,
                    weapon_size=WeaponSize.HEAVY,
                    tradeable=True
                    )

iron_sword = Weapon(name="Iron Sword",
                    effect=8,
                    price=70,
                    weapon_type=WeaponType.SHARP,
                    weapon_size=WeaponSize.LIGHT,
                    tradeable=True
                    )
        
iron_mace = Weapon(name="Iron Mace",
                    effect=9,
                    price=62,
                    weapon_type=WeaponType.BLUNT,
                    weapon_size=WeaponSize.MEDIUM,
                    tradeable=True
                    )
        
fists = Weapon(name="Fists",
                effect=20,
                price=0,
                weapon_type=WeaponType.BLUNT,
                weapon_size=WeaponSize.LIGHT,
                tradeable=False
                )

undead_fists = Weapon(name="Fists of Undead",
                effect=6,
                price=0,
                weapon_type=WeaponType.BLUNT,
                weapon_size=WeaponSize.LIGHT,
                tradeable=False
                )

# Objects of Armour
# Helmets
knight_helmet = Armour(name="Knight Helmet",
                      effect=2,
                      price=75,
                      armour_type=ArmourType.HELMET,
                      armour_size=ArmourSize.MEDIUM,
                      tradeable=True
                      )

mercenary_bascinet = Armour(name="Mercenary Bascinet",
                      effect=1,
                      price=57,
                      armour_type="Helmet",
                      armour_size="Light",
                      tradeable=True
                      )

# Armours
leather_armour = Armour(name="Leather Armour",
                      effect=2,
                      price=96,
                      armour_type="Breastplate",
                      armour_size="Light",
                      tradeable=True
                      )

chain_shirt = Armour(name="Chain Shirt",
                      effect=3,
                      price=108,
                      armour_type="Breastplate",
                      armour_size="Medium",
                      tradeable=True
                      )

damaged_breastplate = Armour(name="Breastplate",
                      effect=3,
                      price=99,
                      armour_type="Breastplate",
                      armour_size="Heavy",
                      tradeable=True
                      )

# Gloves
hunter_gloves = Armour(name="Hunter Gloves",
                      effect=1,
                      price=62,
                      armour_type="Gauntlets",
                      armour_size="Light",
                      tradeable=True
                      )

iron_gauntlets = Armour(name="Iron Gauntlets",
                      effect=2,
                      price=81,
                      armour_type="Gauntlets",
                      armour_size="Medium",
                      tradeable=True
                      )

# Shields
shadow_shield = Armour(name="Shadow_Shield",
                      effect=2,
                      price=105,
                      armour_type="Shield",
                      armour_size="Medium",
                      tradeable=True
                      )

wooden_shield = Armour(name="Wooden Shield",
                      effect=1,
                      price=69,
                      armour_type="Shield",
                      armour_size="Light",
                      tradeable=True
                      )

# Legs
mail_chausses = Armour(name="Mail Chausses",
                      effect=3,
                      price=92,
                      armour_type="Legs",
                      armour_size="Medium",
                      tradeable=True
                      )

green_hose = Armour(name="Green Hose",
                      effect=1,
                      price=42,
                      armour_type="Legs",
                      armour_size="Light",
                      tradeable=True
                      )

# Boots
riding_boots = Armour(name="Riding Boots",
                      effect=1,
                      price=57,
                      armour_type="Boots",
                      armour_size="Light",
                      tradeable=True
                      )

mail_boots = Armour(name="Mail Boots",
                      effect=3,
                      price=107,
                      armour_type="Boots",
                      armour_size="Heavy",
                      tradeable=True
                      )

# Rings
ring_of_live = Armour(name="Ring of Live",
                      effect=5,
                      price=185,
                      armour_type="Ring",
                      armour_size="Light",
                      tradeable=True
                      )

ring_of_duke_william = Armour(name="Ring of Duke William",
                      effect=4,
                      price=259,
                      armour_type="Ring",
                      armour_size="Light",
                      tradeable=True
                      )

# Amulets
amulet_of_saint_church = Armour(name="Amulet of Saint Church",
                      effect=10,
                      price=174,
                      armour_type="Amulet",
                      armour_size="Light",
                      tradeable=True
                      )

start = GameContoller.StartScreen()
menu = GameContoller.MainMenu(start)