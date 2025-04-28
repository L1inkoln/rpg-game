from characters.base import ICharacter
from typing import Sequence
from items.potions import HealthPotion
from levels.level import Battle, Level, Skeleton


# ---Реализация уровня с наградами при прохождении---
class DungeonLevel(Level):
    def __init__(self) -> None:
        enemies = [Skeleton("Скелет 1"), Skeleton("Скелет 2")]
        super().__init__(name="Подземелье", enemies=enemies)

    def start(self, heroes: Sequence[ICharacter]) -> None:
        print(f"🏰 Вы входите в '{self.name}'...")
        print(f"🧟 На пути встают {len(self.enemies)} врагов!\n")

        battle = Battle(heroes, self.enemies)
        battle.start()

        if all(enemy.health <= 0 for enemy in self.enemies):
            self.reward(heroes)
            self._complete()

    def reward(self, heroes: Sequence[ICharacter]) -> None:
        print("\n🎁 Награды за победу:")
        for hero in heroes:
            if hasattr(hero, "add_consumable"):
                hero.add_consumable(HealthPotion())
                print(f"{hero.name} получил Зелье здоровья!")
