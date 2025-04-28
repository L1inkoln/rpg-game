from abc import ABC, abstractmethod


class IAbility(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    def use(self, caster, target) -> None: ...
