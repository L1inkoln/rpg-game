from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from characters.base import ICharacter


# ===== Интерфейс способности =====
class IAbility(ABC):
    @abstractmethod
    def use(self, caster: "ICharacter", target: "ICharacter") -> None: ...


# ===== Базовый класс для декораторов способностей =====
class AbilityDecorator(IAbility):
    def __init__(self, wrapped_ability: IAbility) -> None:
        self._wrapped_ability = wrapped_ability

    def use(self, caster: "ICharacter", target: "ICharacter") -> None:
        self._wrapped_ability.use(caster, target)
