import random


class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Person:

    def __init__(self, name, hp, mp, atk, df, magic, items):
        self.max_hp = hp
        self.hp = hp
        self.max_mp = mp
        self.mp = mp
        self.atk = atk
        self.ath_l = atk - 10
        self.ath_h = atk + 10
        self.df = df
        self.magic = magic
        self.items = items
        self.actions = ["Attack", "Magic", "Items"]
        self.name = name

    def generate_damage(self):
        return random.randrange(self.ath_l, self.ath_h)

    def generate_spell_damage(self, i):
        mg_l = self.magic[i]["dmg"] - 5
        mg_h = self.magic[i]["dmg"] + 5
        return random.randrange(mg_l, mg_h)

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def heal(self, dmg):
        self.hp += dmg
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.max_hp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.max_mp

    def reduce_mp(self, cost):
        self.mp -= cost

    def choose_action(self):
        i = 1
        print("\n" + "\t" + Bcolors.BOLD + self.name + Bcolors.ENDC)
        print(Bcolors.OKBLUE + Bcolors.BOLD + "\nACTIONS" + Bcolors.ENDC)
        for item in self.actions:
            print("\t" + str(i) + ".", item)
            i += 1

    def choose_magic(self):
        i = 1
        print(Bcolors.OKBLUE + Bcolors.BOLD + "\nMAGIC" + Bcolors.ENDC)
        for spell in self.magic:
            print("\t" + str(i) + ".", spell.name, "(cost:", str(spell.cost) + ")")
            i += 1
        print(Bcolors.FAIL + "Press 0 to back" + Bcolors.ENDC)

    def choose_item(self):
        i = 1
        print(Bcolors.OKGREEN + Bcolors.BOLD + "\nITEMS:" + Bcolors.ENDC)
        for item in self.items:
            print("\t" + str(i) + ".", item["item"].name, ":", item["item"].description, " (x" + str(item["quantity"]) + ")")
            i += 1
        print(Bcolors.FAIL + "Press 0 to back" + Bcolors.ENDC)

    def choose_target(self, enemies):
        i = 1
        print("\n" + Bcolors.FAIL + Bcolors.BOLD + "TARGET:" + Bcolors.ENDC)
        for enemy in enemies:
            if enemy.get_hp() != 0:
                print("\t" + str(i) + ".", enemy.name)
                i += 1

        choice = int(input("Choose target:")) - 1

        return choice

    def get_enemy_stats(self):
        hp_bar = ""
        bar_ticks = (self.hp / self.max_hp) * 100 / 2

        while bar_ticks > 0:
            hp_bar += "█"
            bar_ticks -= 1

        while len(hp_bar) < 50:
            hp_bar += " "

        hp_string = str(self.hp) + "/" + str(self.max_hp)
        current_hp = ""
        if len(hp_string) < 11:
            decreased = 11 - len(hp_string)

            while decreased > 0:
                current_hp += " "
                decreased -= 1

            current_hp += hp_string
        else:
            current_hp = hp_string

        print(Bcolors.BOLD + self.name + " HP    " +
              current_hp + " |" + Bcolors.FAIL + hp_bar + Bcolors.ENDC +
              "|      ")

    def get_stats(self):
        hp_bar = ""
        bar_ticks = (self.hp / self.max_hp) * 100 / 4

        mp_bar = ""
        mp_ticks = (self.mp / self.max_mp) * 100 / 10

        while bar_ticks > 0:
            hp_bar += "█"
            bar_ticks -= 1

        while len(hp_bar) < 25:
            hp_bar += " "

        while mp_ticks > 0:
            mp_bar += "█"
            mp_ticks -= 1

        while len(mp_bar) < 10:
            mp_bar += " "

        # print("                        _________________________                ___________ ")
        # print(Bcolors.BOLD + self.name + "    " +
        #       str(self.hp) + "/" + str(self.max_hp) + " |" + Bcolors.OKGREEN + "████████████████" + Bcolors.ENDC +
        #       Bcolors.BOLD + "|      " +
        #       str(self.mp) + "/" + str(self.max_mp) + " |" + Bcolors.OKBLUE + "███████" + "|" + Bcolors.ENDC)

        hp_string = str(self.hp) + "/" + str(self.max_hp)
        current_hp = ""
        if len(hp_string) < 9:
            decreased = 9 - len(hp_string)

            while decreased > 0:
                current_hp += " "
                decreased -= 1

            current_hp += hp_string
        else:
            current_hp = hp_string

        mp_string = str(self.mp) + "/" + str(self.max_mp)
        current_mp = ""
        if len(mp_string) < 7:
            decreased = 7 - len(mp_string)

            while decreased > 0:
                current_mp += " "
                decreased -= 1

            current_mp += mp_string
        else:
            current_mp = mp_string

        print(Bcolors.BOLD + self.name + " HP    " +
              current_hp + " |" + Bcolors.OKGREEN + hp_bar + Bcolors.ENDC +
              "|      ")
        print("          MP      " + Bcolors.BOLD + current_mp + " |" + Bcolors.OKBLUE +
              mp_bar + Bcolors.ENDC + "|" + Bcolors.ENDC)
