from abc import ABC, abstractmethod
from typing import Sequence
from characters.base import ICharacter


# ===== Базовый класс уровня =====
class Level(ABC):
    def __init__(self, name: str, enemies: Sequence[ICharacter]) -> None:
        self._name = name
        self._enemies = enemies
        self._completed = False

    @property
    def name(self) -> str:
        return self._name

    @property
    def enemies(self) -> Sequence[ICharacter]:
        return self._enemies

    @property
    def completed(self) -> bool:
        return self._completed

    def complete(self) -> None:
        self._completed = True
        print(f"Уровень '{self.name}' пройден!")

    @abstractmethod
    def start(self) -> None:
        pass
