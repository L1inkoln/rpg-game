from characters.base import ICharacter
from typing import TYPE_CHECKING

from levels.level import Level

if TYPE_CHECKING:
    from abilities.base import IAbility


class Skeleton(ICharacter):
    def __init__(self) -> None:
        self._health = 30
        self._name = "Скелет"
        self._abilities: list["IAbility"] = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def health(self) -> int:
        return self._health

    def take_damage(self, damage: int) -> None:
        self._health = max(0, self._health - damage)
        print(f"{self.name} получил {damage} урона!")

    def add_ability(self, ability: "IAbility") -> None:
        self._abilities.append(ability)

    def use_ability(self, index: int, target: "ICharacter") -> None:
        if 0 <= index < len(self._abilities):
            self._abilities[index].use(self, target)
        else:
            print(f"{self.name} не смог использовать способность.")


class DungeonLevel(Level):
    def __init__(self) -> None:
        enemies = [Skeleton(), Skeleton()]
        super().__init__(name="Подземелье", enemies=enemies)

    def start(self) -> None:
        print(f"Вы входите в '{self.name}'...")
        print(f"На пути встают {len(self.enemies)} врагов!")
