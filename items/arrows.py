from characters.base import ICharacter
from items.base import IConsumable
from levels.base import IEnemy


# ---Базовая стрела---
class Arrow(IConsumable):
    def __init__(self, name: str = "Стрела", damage: int = 5):
        self._name = name
        self._damage = damage
        self._max_stack = 10

    @property
    def name(self) -> str:
        return self._name

    @property
    def max_stack(self) -> int:
        return self._max_stack

    @property
    def damage(self) -> int:
        return self._damage

    def consume(self) -> dict:
        return {"damage": self._damage}

    def apply_effect(self, target: ICharacter | IEnemy) -> None:
        pass


class FrostArrow(Arrow):
    def __init__(self):
        super().__init__(name="Ледяная стрела", damage=10)

    def apply_effect(self, target) -> None:
        print(f"{target.name} замедлен!")


class FireArrow(Arrow):
    def __init__(self):
        super().__init__(name="Огненная стрела", damage=10)

    def apply_effect(self, target) -> None:
        print(f"{target.name} горит и получает доп. урон!")
        target.take_damage(5)  # Доп урон от горения
