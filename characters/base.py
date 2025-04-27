from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

from abilities.base import IAbility


# ===== Статы персонажа =====
@dataclass(frozen=True)
class Stats:
    strength: int = 10
    agility: int = 10
    intelligence: int = 10


# ===== Интерфейс персонажа =====
class ICharacter(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def health(self) -> int: ...

    @abstractmethod
    def take_damage(self, damage: int) -> None: ...

    @abstractmethod
    def add_ability(self, ability: IAbility) -> None: ...

    @abstractmethod
    def use_ability(self, index: int, target: "ICharacter") -> None: ...


# ===== Базовый класс персонажа =====
class Character(ICharacter):
    MAX_HEALTH = 100

    def __init__(self, name: str, stats: Stats) -> None:
        self._name = name
        self._stats = stats
        self._health = self.MAX_HEALTH
        self._abilities: List[IAbility] = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def health(self) -> int:
        return self._health

    @property
    def stats(self) -> Stats:
        return self._stats

    def take_damage(self, damage: int) -> None:
        self._health = max(0, self._health - damage)
        print(f"{self.name} получил {damage} урона! (HP: {self._health})")

    def heal(self, amount: int) -> None:
        self._health = min(self.MAX_HEALTH, self._health + amount)
        print(f"{self.name} восстановил {amount} HP! (HP: {self._health})")

    def add_ability(self, ability: IAbility) -> None:
        self._abilities.append(ability)

    def use_ability(self, index: int, target: "ICharacter") -> None:
        if 0 <= index < len(self._abilities):
            self._abilities[index].use(self, target)
        else:
            print(f"{self.name} не имеет способности под номером {index}.")
