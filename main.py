from Classes.game import Person, Bcolors
from Classes.spells import Spell
from Classes.inventory import Item
import random


# Crate Black Magic
fire = Spell("Fire Ball", 25, 600, "black")
thunder = Spell("Thunder Bolt", 25, 600, "black")
blizzard = Spell("Blizzard", 25, 600, "black")
meteor = Spell("Meteor", 40, 1200, "black")
quake = Spell("Quake", 14, 120, "black")

# Create white magic
cure = Spell("Cure", 25, 620, "white")
cura = Spell("Cura", 32, 1500, "white")

# Create new Items
potion = Item("Potion", "potion", "Heals 50 HP", 200)
hiPotion = Item("Hi-Potion", "potion", "Heals 100 HP", 500)
superPotion = Item("Super Potion", "potion", "Heals 500 HP", 1000)
elixir = Item("Elixir", "elixir", "Fully restores HP/MP", 9999)
megaElixir = Item("MegaElixir", "elixir", "Fully restores party's HP/MP", 9999)

scrollOfFire = Item("Scroll of Fire", "attack", "Deals 500 damage", 500)

player_spells = [fire, thunder, blizzard, meteor, quake, cure, cura]
player_items = [{"item": potion, "quantity": 5}, {"item": hiPotion, "quantity": 3},
                {"item": superPotion, "quantity": 2}, {"item": elixir, "quantity": 2},
                {"item": megaElixir, "quantity": 1}, {"item": scrollOfFire, "quantity": 5}]

enemy_spells = [fire, meteor, cure]
enemy_items = []

player1 = Person("Yubei    ", 3260, 132, 300, 34, player_spells, player_items)
player2 = Person("Hiridrim ", 4160, 188, 311, 34, player_spells, player_items)
player3 = Person("Jaina    ", 3089, 174, 288, 34, player_spells, player_items)

enemy = Person("BIG BOSS ", 11200, 2210, 525, 25, enemy_spells, enemy_items)
enemy2 = Person("Imp      ", 1250, 130, 560, 325, enemy_spells, enemy_items)
enemy3 = Person("Imp      ", 1250, 130, 560, 325, enemy_spells, enemy_items)

players = [player1, player2, player3]
enemies = [enemy, enemy2, enemy3]

running = True

print(Bcolors.FAIL + Bcolors.BOLD + enemy.name + " ATTACKS!" + Bcolors.ENDC)
print("Enemy HP: ", enemy.get_max_hp())

while running:
    print("===========================")

    print("\n")

    for player in players:
        player.get_stats()

    print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        player.choose_action()
        choice = input("Choose action:")
        index = int(choice) - 1
        # print("You chose", index)

        if index == 0:
            print("You choose to attack!")
            print("----------------------------------")
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(dmg)
            print("You attacked " + enemies[enemy].name.replace(" ", "") + " for:", dmg)

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name + " has died.")
                del enemies[enemy]

        elif index == 1:
            mp = player.get_mp()
            player.choose_magic()
            print("Player MP:", Bcolors.OKBLUE + str(player.get_mp()) + "/" + str(player.get_max_mp()) + Bcolors.ENDC)
            choice = input("Choose spell: ")
            magic_choice = int(choice) - 1
            if magic_choice == -1:
                continue
            spell = player.magic[magic_choice]
            spell_dmg = spell.generate_damage()
            if spell.cost <= mp:
                print("You casted " + Bcolors.OKBLUE + str(spell.name) + Bcolors.ENDC)
                print("----------------------------------")
                if spell.category == "white":
                    player.heal(spell_dmg)
                    print("You healed yourself for", spell_dmg)
                elif spell.category == "black":
                    enemy = player.choose_target(enemies)
                    enemies[enemy].take_damage(spell_dmg)

                    print("You attacked " + enemies[enemy].name.replace(" ", "") + " for:", spell_dmg)

                    if enemies[enemy].get_hp() == 0:
                        print(enemies[enemy].name + " has died.")
                        del enemies[enemy]

                player.reduce_mp(spell.cost)
            else:
                print(Bcolors.BOLD + "Not enough MP!" + Bcolors.ENDC)
                continue

        elif index == 2:
            player.choose_item()
            item_choice = int(input("Choose item: ")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(Bcolors.FAIL + "\n" + "No items" + Bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.category == "potion":
                player.heal(item.prop)
                print(Bcolors.OKGREEN + "\n" + item.name + " heals for", str(item.prop), "HP" + Bcolors.ENDC)

            elif item.category == "elixir":

                if item.name == "MegaElixir":
                    for allPlayers in players:
                        allPlayers.hp = allPlayers.max_hp
                        allPlayers.mp = allPlayers.max_mp
                else:
                    player.hp = player.max_hp
                    player.mp = player.max_mp
                print(Bcolors.OKGREEN + "\n" + item.name + " Fully restores HP/MP" + Bcolors.ENDC)

            elif item.category == "attack":

                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)

                print(Bcolors.FAIL + "\n" + item.name + " deals", str(item.prop), "point of damage to " + enemies[enemy].name.replace(" ", "") + Bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died.")
                    del enemies[enemy]
                elif len(enemies) == 0:
                    print(Bcolors.OKGREEN + "You win!" + Bcolors.ENDC)
                    running = False

    # enemy phase
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)

        if enemy_choice == 0:
            if len(players) == 0:
                print(Bcolors.FAIL + "You loose!" + Bcolors.ENDC)
                running = False
            else:
                target = random.randrange(0, len(players))
                print("Player " + players[target].name.replace(" ", "") + " has been hit!")
                enemy_dmg = enemy.generate_damage()
                players[target].take_damage(enemy_dmg)

                print(enemy.name.replace(" ", "") + " attacked " + players[target].name.replace(" ", "") + " for", enemy_dmg)
                print("----------------------------------")

        elif enemy_choice == 1:
            magic_choice = random.randrange(0, len(enemy_spells))
            spell = enemy_spells[magic_choice]
            spell_dmg = spell.generate_damage()
            if spell.cost <= enemy.mp:

                enemy.reduce_mp(spell.cost)

                if spell.category == "white":
                    enemy.heal(spell_dmg)
                    print(Bcolors.OKBLUE + "\n" + enemy.name.replace(" ", "") + " casted " + spell.name +
                          " and healed for", str(spell_dmg), "HP." + Bcolors.ENDC)

                elif spell.category == "black":
                    if len(players) == 0:
                        print(Bcolors.FAIL + "You loose!" + Bcolors.ENDC)
                        running = False
                    else:
                        target = random.randrange(0, len(players))
                        print(str(len(players)))
                        players[target].take_damage(spell_dmg)

                        print(Bcolors.OKBLUE + "\n" + enemy.name.replace(" ", "") + " casted " + spell.name +
                              " and deals", str(spell_dmg) + " to " + players[target].name)

                        if players[target].get_hp() == 0:
                            print(players[target].name.replace(" ", "") + " has died.")
                            del players[target]
            else:
                print(enemy.name + " has no MP!")
                continue


