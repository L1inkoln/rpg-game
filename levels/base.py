from abc import ABC, abstractmethod
from typing import List

from abilities.base import IAbility
from characters.base import Stats


# ---Интерфейс для врагов на уровнях ---
class IEnemy(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def health(self) -> int: ...

    @property
    @abstractmethod
    def stats(self) -> Stats: ...

    @abstractmethod
    def attack(self, target) -> None: ...

    @abstractmethod
    def take_damage(self, damage: int) -> None: ...

    @abstractmethod
    def use_ability(self, index: int, target) -> None: ...

    @property
    @abstractmethod
    def abilities(self) -> List[IAbility]: ...
