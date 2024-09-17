class Monster:
    def __init__(self, energy, health, **kwargs):
        super().__init__(**kwargs)
        self.energy = energy
        self.health = health

class Fish():
    def __init__(self, speed, **kwargs):
        super().__init__(**kwargs)
        self.speed = speed

class Shark(Monster, Fish):
    def __init__(self, teeth, **kwargs):
        super().__init__(**kwargs)
        self.teeth = teeth
    def __repr__(self):
        return f"Shark(energy = {self.energy}, health = {self.health}, speed = {self.speed}, teeth = {self.teeth})"

shark = Shark(energy = 10, health = 15, speed = 20, teeth = 30)
# the super().__init__(**kwargs) it's useful to navigate the mro (method resolution order) and pass **kwargs remaining arguments
# to the following methods.
print(shark)
print(Shark.mro())