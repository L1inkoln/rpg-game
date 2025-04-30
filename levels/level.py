from abc import ABC, abstractmethod
import random
import re
from typing import Sequence, Union
from abilities.abilites import Fireball
from characters.base import ICharacter, Stats
from items.weapons import LordSword
from levels.base import IEnemy


# ---Базовый класс для создания уровней---
class Level(ABC):
    def __init__(self, name: str, enemies: Sequence[IEnemy]) -> None:
        self._name = name
        self._enemies = list(enemies)  # чтобы можно было изменять
        self._completed = False

    @property
    def name(self) -> str:
        return self._name

    @property
    def enemies(self) -> list[IEnemy]:
        return self._enemies

    @property
    def completed(self) -> bool:
        return self._completed

    def _complete(self) -> None:
        self._completed = True
        print(f"\n🏆 Уровень '{self.name}' пройден!")

    @abstractmethod
    def start(self, heroes: Sequence[ICharacter]) -> None:
        """Запустить уровень с героями."""
        ...


# ---Реализация врага(скелет)---
class Skeleton(IEnemy):
    def __init__(self, name) -> None:
        self._health = 30
        self._stats = Stats(strength=5, agility=3, intelligence=3)
        self._name = name
        self._abilities: list = []
        self._damage = 10  # Урон скелета (фиксированный урон мечом)
        self._weapon = "Меч"  # Условное оружие

    @property
    def name(self) -> str:
        return self._name

    @property
    def health(self) -> int:
        return self._health

    @property
    def stats(self) -> Stats:
        return self._stats

    def attack(self, target: ICharacter) -> None:
        # Простой фиксированный урон
        print(f"{self.name} атакует {target.name} мечом! (Урон: {self._damage})")
        target.take_damage(self._damage)

    def take_damage(self, damage: int) -> None:
        self._health = max(0, self._health - damage)
        print(f"{self.name} получил {damage} урона! (HP: {self._health})")
        if self._health <= 0:
            print(f"{self.name} убит!")

    def use_ability(self, index: int, target: ICharacter) -> None:
        if 0 <= index < len(self._abilities):
            self._abilities[index].use(self, target)
        else:
            print(f"{self.name} не смог использовать способность.")

    @property
    def abilities(self) -> list:
        return self._abilities


# Босс на уровне с способностью fireball
class DarkLord(IEnemy):

    def __init__(self):
        self._stats = Stats(strength=50, agility=30, intelligence=40)
        self._name = "Темный Лорд"
        self._health = 200
        self._damage = 20
        self._abilities = [Fireball()]
        self._weapon = LordSword()

    @property
    def name(self) -> str:
        return f"{'\033[91m'}{self._name}{'\033[0m'}"

    @property
    def health(self) -> int:
        return self._health

    @property
    def stats(self) -> Stats:
        return self._stats

    def attack(self, target: ICharacter) -> None:
        weapon_damage = self._weapon.damage if self._weapon else 0
        damage = self._stats.strength // 2 + weapon_damage
        print(
            f"{self.name} взял {self._weapon.name} и аткаовал {target.name}{'\033[92m'}а!{'\033[0m'}  (Урон: {damage})"
        )
        target.take_damage(self._damage)

    def take_damage(self, damage: int) -> None:
        self._health = max(0, self._health - damage)
        print(f"{self.name} получает {damage} урона! (HP: {self._health})")
        if self._health <= 0:
            print(f"Босс замка {self.name} повержен!")

    def use_ability(self, index: int, target: ICharacter) -> None:
        if 0 <= index < len(self._abilities):
            self.use_ability(0, target)

    @property
    def abilities(self) -> list:
        return self._abilities


# Класс для вывода логов о бое
class BattleLogger:
    def __init__(self):
        self.logs = []

    def _strip_ansi(self, text: str) -> str:
        return re.sub(r"\x1b\[[0-9;]*m", "", text)

    def log_action(self, actor: str, target: str, action: str):
        clean_actor = self._strip_ansi(actor)
        clean_target = self._strip_ansi(target)
        clean_action = self._strip_ansi(action)
        self.logs.append((clean_actor, clean_target, clean_action))

    def print_summary(self):
        print("\n📜 Итоговая таблица боя:\n")
        print("┌────────────────┬────────────────┬─────────────────────┐")
        print("│ Персонаж       │ Цель           │      Действие       │")
        print("├────────────────┼────────────────┼─────────────────────┤")
        for actor, target, action in self.logs:
            print(f"│ {actor:<14} │ {target:<14} │ {action:<19} │")
        print("└────────────────┴────────────────┴─────────────────────┘")


# Класс для битвы на уровнях
class Battle:
    def __init__(self, heroes: Sequence[ICharacter], enemies: Sequence[IEnemy]):
        self.heroes = heroes
        self.enemies = enemies
        self.logger = BattleLogger()

    def start(self) -> None:
        print("\n ⚔️ Начинается битва!")
        all_combatants = list(self.heroes) + list(self.enemies)
        round_counter = 1
        while any(hero.health > 0 for hero in self.heroes) and any(
            enemy.health > 0 for enemy in self.enemies
        ):
            print(f"\n✨ Раунд {round_counter}")
            for character in all_combatants:
                if character.health <= 0:
                    continue  # Мертвые пропускают ход
                self.character_action(character)
            round_counter += 1

        if all(enemy.health <= 0 for enemy in self.enemies):
            print("\n✅ Вы победили всех врагов!")
        else:
            print("\n❌ Ваши герои проиграли...")

        self.logger.print_summary()

    # Псевдорандомная логика действий персонажей и врагов
    def character_action(self, character: ICharacter | IEnemy) -> None:
        target_list = self.enemies if character in self.heroes else self.heroes
        target = self.choose_target(target_list)
        if target:
            # 20% шанс использовать способность, если она есть
            use_ability = (
                hasattr(character, "abilities")
                and character.abilities
                and random.random() < 0.8
            )

            if use_ability:
                ability = random.choice(character.abilities)
                self.logger.log_action(character.name, target.name, ability.name)
                ability.use(character, target)
            else:
                self.logger.log_action(character.name, target.name, "Обычная атака")
                character.attack(target)

    def choose_target(
        self, targets: Sequence[ICharacter | IEnemy]
    ) -> Union[ICharacter, IEnemy, None]:
        alive = [t for t in targets if t.health > 0]
        return random.choice(alive) if alive else None
