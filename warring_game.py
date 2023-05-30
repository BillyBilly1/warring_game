import math
import datetime
"""FDHFSID"""
#JNTM
class BuildingMoveError(Exception):
    pass


class WallAttackError(Exception):
    pass


class Player:

    name: str
    unit: list
    coins: int
    food: int

    def __init__(self, name: str, coins: int, food_num: int) -> None:
        self.name = name
        self.unit = []
        self.coins = coins
        self.food = food_num


class CombatUnit:
    """A class for the types of each box"""

    x: int
    y: int
    camps: Player
    hp: float
    attack: float
    m_range: int  # m stands for movement
    a_range: tuple[int, int]  # a stands for attack
    d_range: tuple[int, int]  # d stands for damage
    hiring_cost: int
    food: int

    def __init__(self, x: int, y: int, camps: Player) -> None:
        self.x = x
        self.y = y
        self.camps = camps

    def move(self, x: int, y: int) -> bool:
        """Check whether the movement is valid, and the new coordinate"""
        dx = abs(x - self.x)
        dy = abs(x - self.y)
        if dx > self.m_range or dy > self.m_range or not (bool(dx) ^ bool(dy)):
            return False
        else:
            self.x = x
            self.y = y
            return True

    def be_attacked(self, attack: float) -> bool:
        """Update the units' hp and check whether it is  dead"""
        self.hp -= attack
        return self.hp > 0


class MeleeUnit(CombatUnit):

    def __init__(self, x: int, y: int, camps: Player) -> None:
        super().__init__(x, y, camps)
        self.m_range = 2
        self.a_range = 3, 3
        self.d_range = 1, 1
        self.food = 5

    def get_attackable_range(self) -> None:
        pass

    def get_damage_positions(self) -> None:
        pass


class Spearman(MeleeUnit):
    def __init__(self, x: int, y: int, camps: Player) -> None:
        super().__init__(x, y, camps)
        self.hp = 5.0
        self.attack = 3.0
        self.hiring_cost = 100


class ShieldedSpearman(Spearman):
    def __init__(self, x: int, y: int, camps: Player) -> None:
        super().__init__(x, y, camps)
        self.hp = 6.0
        self.hiring_cost = 130


class Hammerman(MeleeUnit):
    def __init__(self, x: int, y: int, camps: Player) -> None:
        super().__init__(x, y, camps)
        self.hp = 5.5
        self.attack = 3.75
        self.hiring_cost = 160


class ShieldedHammerman(MeleeUnit):
    def __init__(self, x: int, y: int, camps: Player) -> None:
        super().__init__(x, y, camps)
        self.hp = 6.5
        self.attack = 3.75
        self.hiring_cost = 200


class SwordMan(MeleeUnit):
    armour: bool

    def __init__(self, x: int, y: int, camps: Player, armour: bool) -> None:
        super().__init__(x, y, camps)
        self.armour = armour
        self.hp = 6.5
        self.attack = 3.75
        self.hiring_cost = 250
        if self.armour:
            self.hiring_cost += 30

    def be_attacked(self, attack: float) -> bool:
        if self.armour:
            self.hp -= (attack * 0.8)
        else:
            self.hp -= attack
        return self.hp > 0


class ShieldedSwordMan(SwordMan):
    def __init__(self, x: int, y: int, camps: Player, armour: bool) -> None:
        super().__init__(x, y, camps, armour)
        self.armour = armour
        self.hp = 7.25
        self.hiring_cost = 290


class Building(CombatUnit):
    """Non-movable Combat Unit, may or may not be able to attack"""

    def __init__(self, x: int, y: int, camps: Player) -> None:
        super().__init__(x, y, camps)
        self.food = 0

    def move(self, x: int, y: int) -> bool:
        raise BuildingMoveError


class Wall(Building):
    pass


class WoodenFence(Wall):
    def __init__(self, x: int, y: int, camps: Player) -> None:
        super().__init__(x, y, camps)
        self.hp = 4.5
        self.hiring_cost = 45


class ThornBush(Wall):
    def __init__(self, x: int, y: int, camps: Player) -> None:
        super().__init__(x, y, camps)
        self.hp = 1.0
        self.attack = 1.25
        self.a_range = 3, 3
        self.d_range = 1, 1
        self.hiring_cost = 65


class StoneWall(Wall):
    def __init__(self, x: int, y: int, camps: Player) -> None:
        super().__init__(x, y, camps)
        self.hp = 6.5
        self.hiring_cost = 90


class IronWall(Wall):
    def __init__(self, x: int, y: int, camps: Player) -> None:
        super().__init__(x, y, camps)
        self.hp = 8.5
        self.hiring_cost = 145


class DiamondWall(Wall):
    def __init__(self, x: int, y: int, camps: Player) -> None:
        super().__init__(x, y, camps)
        self.hp = 11
        self.attack = 0.5
        self.a_range = 3, 3
        self.d_range = 1, 1
        self.hiring_cost = 200


# ============================================================================#


if __name__ == '__main__':
    s = Spearman(1, 2, Player())
    s.move(4, 2)
    print(s.x)
    print(s.y)
    a = s.be_attacked(9.0)
    print(s.hp)
    print(a)
