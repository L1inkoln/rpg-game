from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from characters.base import Character


# ===== Интерфейс предмета =====
class InventoryItem(ABC):
    @abstractmethod
    def use(self, character: "Character") -> None: ...
