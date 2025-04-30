from characters.base import ICharacter, Stats
from characters.character import Character
from items.weapons import Knife, Sword, Weapon
from levels.level import IEnemy


class Warrior(Character):
    def __init__(self, name: str):
        super().__init__(name, Stats(strength=18, agility=8, intelligence=5))

    def attack(self, target: ICharacter | IEnemy) -> None:
        if not isinstance(self._weapon, Sword):
            print(f"У {self.name} нет меча!")
            super().attack(target)
            return

        damage = self._calculate_damage()
        print(
            f"{self.name} взял {self._weapon.name} и ударил {target.name}! (Урон: {damage})"
        )
        target.take_damage(damage)

    def can_equip_weapon(self, weapon: Weapon) -> bool:
        return isinstance(weapon, Sword | Knife)
