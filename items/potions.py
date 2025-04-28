from items.base import IConsumable


class HealthPotion(IConsumable):
    def __init__(self, heal_amount: int = 15):
        self._heal_amount = heal_amount
        self._max_stack = 5

    @property
    def name(self) -> str:
        return f"Зелье здоровья (+{self._heal_amount} HP)"

    @property
    def max_stack(self) -> int:
        return self._max_stack

    def consume(self) -> dict:
        print(f"использовано {self.name}")
        return {"heal": self._heal_amount}


class DamagePotion(IConsumable):
    def __init__(self, damage_buff: int = 5):
        self._damage_buff = damage_buff
        self._max_stack = 5

    @property
    def name(self) -> str:
        return f"Зелье ярости (+{self._damage_buff} урона)"

    @property
    def max_stack(self) -> int:
        return self._max_stack

    def consume(self) -> dict:
        return {"damage_buff": self._damage_buff}
