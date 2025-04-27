from abc import ABC, abstractmethod


class InventoryItem(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...


class IConsumable(InventoryItem):
    @property
    @abstractmethod
    def max_stack(self) -> int: ...

    @abstractmethod
    def consume(self) -> dict: ...
