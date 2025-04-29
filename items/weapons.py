from items.base import InventoryItem


class Weapon(InventoryItem):
    def __init__(self, name: str, damage: int):
        self._name = name
        self._damage = damage

    @property
    def name(self) -> str:
        return f"{'\033[34m'}{self._name}{'\033[0m'}"

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


class LordSword(Weapon):
    def __init__(self):
        super().__init__(name="Меч лорда", damage=30)

    @property
    def name(self) -> str:
        return f"{'\033[35m'}{self._name}{'\033[0m'}"
