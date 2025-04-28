from abc import ABC, abstractmethod
import random
from typing import List, Sequence, Union

from abilities.base import IAbility
from characters.base import ICharacter


# ---Интерфейс для врагов на уровнях ---
class IEnemy(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def health(self) -> int: ...

    @abstractmethod
    def attack(self, target) -> None: ...

    @abstractmethod
    def take_damage(self, damage: int) -> None: ...

    @abstractmethod
    def add_ability(self, ability: IAbility) -> None: ...

    @abstractmethod
    def use_ability(self, index: int, target: "ICharacter") -> None: ...

    @property
    @abstractmethod
    def abilities(self) -> List[IAbility]: ...


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

    def attack(self, target: ICharacter) -> None:
        # Простой фиксированный урон
        print(f"{self.name} атакует {target.name} мечом! (Урон: {self._damage})")
        target.take_damage(self._damage)

    def take_damage(self, damage: int) -> None:
        self._health = max(0, self._health - damage)
        print(f"{self.name} получил {damage} урона! (HP: {self._health})")
        if self._health <= 0:
            print(f"{self.name} убит!")

    def add_ability(self, ability) -> None:
        self._abilities.append(ability)

    def use_ability(self, index: int, target: ICharacter) -> None:
        if 0 <= index < len(self._abilities):
            self._abilities[index].use(self, target)
        else:
            print(f"{self.name} не смог использовать способность.")

    @property
    def abilities(self) -> list:
        return self._abilities


# Функция для вывода логов о бое
class BattleLogger:
    def __init__(self):
        self.logs = []

    def log_action(self, actor: str, target: str, action: str):
        self.logs.append((actor, target, action))

    def print_summary(self):
        print("\n📜 Итоговая таблица боя:\n")
        print("┌──────────────┬────────────┬────────────────────┐")
        print("│ Персонаж     │ Цель       │ Действие           │")
        print("├──────────────┼────────────┼────────────────────┤")
        for actor, target, action in self.logs:
            print(f"│ {actor:<12} │ {target:<10} │ {action:<18} │")
        print("└──────────────┴────────────┴────────────────────┘")


class Battle:
    def __init__(self, heroes: Sequence[ICharacter], enemies: Sequence[IEnemy]):
        self.heroes = heroes
        self.enemies = enemies
        self.logger = BattleLogger()

    def start(self) -> None:
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

    def character_action(self, character: Union[ICharacter, IEnemy]) -> None:
        target_list = self.enemies if character in self.heroes else self.heroes
        target = self.choose_target(target_list)
        if target:
            if hasattr(character, "use_random_ability") and character.abilities:
                ability = random.choice(character.abilities)
                self.logger.log_action(character.name, target.name, ability.name)
                ability.use(character, target)
            else:
                self.logger.log_action(character.name, target.name, "Обычная атака")
                character.attack(target)

    def choose_target(
        self, targets: Sequence[Union[ICharacter, IEnemy]]
    ) -> Union[ICharacter, IEnemy, None]:
        alive = [t for t in targets if t.health > 0]
        return random.choice(alive) if alive else None
