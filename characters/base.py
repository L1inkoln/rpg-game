from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Type, TYPE_CHECKING

if TYPE_CHECKING:
    from items.base import IConsumable
    from abilities.base import IAbility


@dataclass(frozen=True)
class Stats:
    strength: int = 10
    agility: int = 10
    intelligence: int = 10


class ICharacter(ABC):
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
    def take_damage(self, damage: int) -> None: ...

    @abstractmethod
    def attack(self, target) -> None: ...

    @abstractmethod
    def can_equip_weapon(self, weapon) -> bool: ...

    # Система предметов
    @abstractmethod
    def _add_consumable(self, item: IConsumable) -> None: ...

    @abstractmethod
    def use_consumable(self, item_type: Type[IConsumable]) -> None: ...

    @abstractmethod
    def get_consumable_count(self, item_type: Type[IConsumable]) -> int: ...

    # Система способностей
    @abstractmethod
    def _add_ability(self, ability: IAbility) -> None: ...

    @abstractmethod
    def use_ability(self, ability: IAbility, target: ICharacter) -> None: ...

    @property
    @abstractmethod
    def abilities(self) -> List[IAbility]: ...
