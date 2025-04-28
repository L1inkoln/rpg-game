from characters.base import ICharacter
from items.base import InventoryItem


class Weapon(InventoryItem):
    def __init__(self, name: str, damage: int):
        self._name = name
        self._damage = damage

    @property
    def name(self) -> str:
        return self._name

    @property
    def damage(self) -> int:
        return self._damage

    def apply_damage(self, target: ICharacter, damage: int) -> None:
        target.take_damage(damage)


class Sword(Weapon):
    def __init__(self):
        super().__init__(name="Меч", damage=15)

    def can_equip(self, character: ICharacter) -> bool:
        return character.__class__.__name__ == "Warrior"


class Bow(Weapon):
    def __init__(self):
        super().__init__(name="Лук", damage=8)

    def can_equip(self, character: ICharacter) -> bool:
        return character.__class__.__name__ == "Archer"


class Staff(Weapon):
    def __init__(self):
        super().__init__(name="Посох", damage=5)

    def can_equip(self, character: ICharacter) -> bool:
        return character.__class__.__name__ == "Mage"


class Dagger(Weapon):
    def __init__(self):
        super().__init__(name="Кинжал", damage=6)

    def can_equip(self, character: ICharacter) -> bool:
        return True  # Для любого класса
