from typing import Sequence
from characters.base import ICharacter
from items.potions import DamagePotion
from levels.level import Battle, DarkLord, Level


class CastleLevel(Level):
    def __init__(self) -> None:
        boss = DarkLord()
        super().__init__(name="Экстремальный уровень: Замок", enemies=[boss])

    def start(self, heroes: Sequence[ICharacter]) -> None:
        print(f"\n{'\033[91m'}⚠️ ЭКСТРИМАЛЬНЫЙ УРОВЕНЬ: '{self.name}'!{'\033[0m'}")
        print(f"🏰 В замок зашли: {', '.join(hero.name for hero in heroes)} ...")
        print(f"👑 На троне сидит босс: {self.enemies[0].name} с огненной магией!\n")

        battle = Battle(heroes, self.enemies)
        battle.start()

        if all(enemy.health <= 0 for enemy in self.enemies):
            self.reward(heroes)
            self._complete()

    def reward(self, heroes: Sequence[ICharacter]) -> None:
        print("\n👑 За победу над боссом вы получаете редкий артефакт!")
        for hero in heroes:
            hero._add_consumable(DamagePotion())
