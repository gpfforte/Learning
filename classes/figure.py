import os
import random


class Character:
    def __init__(self, name, defense, power, health) -> None:
        self.name = name
        self.defense = defense
        self.power = power
        self.health = health
        self.max_health = health

    def attack(self, other):
        self.health = self.health - other.defense * random.randint(0, 2)
        other.health = other.health - self.power * random.randint(0, 2)
        if self.health < 0:
            self.health = 0
        if other.health < 0:
            other.health = 0

    def __str__(self) -> str:
        return f"{self.name} ha {self.health} di salute"


char1 = Character("Ugo", 5, 10, 100)
char2 = Character("Ago", 7, 8, 100)
while True:
    risposta = input("Vuoi Continuare?")
    os.system("cls" if os.name == "nt" else "clear")
    if risposta == "NO":
        break
    char1.attack(char2)
    print(char1)
    print(char2)
    char2.attack(char1)
    print(char1)
    print(char2)

