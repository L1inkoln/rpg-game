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


# Нож для всех классов
class Knife(Weapon): ...


class Sword(Weapon):
    def __init__(self):
        super().__init__(name="Меч", damage=12)


class Bow(Weapon):
    def __init__(self):
        super().__init__(name="Лук", damage=8)


class Staff(Weapon):
    def __init__(self):
        super().__init__(name="Посох", damage=4)


class Dagger(Knife):
    def __init__(self):
        super().__init__(name="Кинжал", damage=6)
