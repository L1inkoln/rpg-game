from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from characters.base import ICharacter


class IAbility(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def use(self, caster: "ICharacter", target: "ICharacter") -> None: ...
