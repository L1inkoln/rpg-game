from __future__ import annotations
import random
from typing import Dict, List, Type, Union
from abilities.base import IAbility
from characters.base import ICharacter, Stats
from items.base import IConsumable
from items.weapons import Knife, Weapon
from levels.base import IEnemy


class Character(ICharacter):
    MAX_HEALTH = 100

    def __init__(self, name: str, stats: Stats):
        self._name = name
        self._stats = stats
        self._health: int = self.MAX_HEALTH
        self._weapon: Weapon = None  # type: ignore
        self._consumables: Dict[Type[IConsumable], List[IConsumable]] = {}
        self._abilities: List[IAbility] = []
        self._active_buffs: Dict[str, int] = {}

    # Базовые свойства
    @property
    def name(self) -> str:
        return f"{'\033[92m'}{self._name}{'\033[0m'}"

    @property
    def health(self) -> int:
        return self._health

    @property
    def stats(self) -> Stats:
        return self._stats

    # Боевая система
    def take_damage(self, damage: int) -> None:
        self._health = max(0, self._health - damage)
        print(f"{self.name} получил {damage} урона! (HP: {self._health})")
        if self._health <= 0:
            print(f"{self.name} убит!")

    def heal(self, amount: int) -> None:
        self._health = self._health + amount
        print(f"{self.name} восстановил {amount} HP!")

    def equip_weapon(self, weapon: Weapon) -> None:
        """Экипировать оружие"""
        if not self.can_equip_weapon(weapon):
            print(f"{self.name} не может использовать {weapon.name}!")
            return

        self._weapon = weapon
        print(f"{self.name} экипировал {weapon.name}!")

    def attack(self, target: ICharacter | IEnemy) -> None:
        damage = self._calculate_damage()
        if isinstance(self._weapon, Weapon):
            print(
                f"{self.name} взял {self._weapon.name} и атаковал {target.name}  (Урон: {damage})"
            )
            target.take_damage(damage)
            return

        if isinstance(self._weapon, Knife):
            print(f"{self.name} быстро ударил {target.name} ножом (Урон: {damage})")
            target.take_damage(damage)
            return

        else:
            print(f"{self.name} атакует кулаками! (Урон: {damage})")
            target.take_damage(damage)

    def _calculate_damage(self) -> int:
        """Базовый расчёт урона без учёта стрел"""
        base_damage = self._stats.strength // 2
        weapon_damage = self._weapon.damage if self._weapon else 0
        buff_damage = self._active_buffs.get("damage", 0)
        return base_damage + weapon_damage + buff_damage

    # Система предметов
    def _add_consumable(self, item: IConsumable) -> None:
        item_type = type(item)
        if item_type not in self._consumables:
            self._consumables[item_type] = []

        if len(self._consumables[item_type]) < item.max_stack:
            self._consumables[item_type].append(item)
            print(f"{self.name} получил предмет: {item.name}")
        else:
            print(f"Нельзя носить больше {item.max_stack} {item.name}!")

    def use_consumable(self, item_type: Type[IConsumable]) -> None:
        if item_type not in self._consumables or not self._consumables[item_type]:
            print(f"Нет {item_type.__name__} в инвентаре!")
            return

        item = self._consumables[item_type].pop()
        effects = item.consume()

        if "heal" in effects:
            self.heal(effects["heal"])
        if "damage_buff" in effects:
            self._active_buffs["damage"] = effects["damage_buff"]
            print(
                f"{self.name} увеличил урон на {effects['damage_buff']} до конца уровня!"
            )

    def get_consumable_count(self, item_type: Type[IConsumable]) -> int:
        count = 0
        for stored_type, items in self._consumables.items():
            if issubclass(stored_type, item_type):
                count += len(items)
        return count

    # Система способностей
    def _add_ability(self, ability: IAbility) -> None:
        self._abilities.append(ability)
        print(f"{self.name} получил способность: {ability.name}")

    def use_ability(
        self, ability: Union[IAbility, type], target: ICharacter | IEnemy
    ) -> None:
        # Если передается класс способности (тип)
        if isinstance(ability, type):
            ability_instance = next(
                (a for a in self._abilities if isinstance(a, ability)), None
            )
            if ability_instance:
                ability_instance.use(self, target)
            else:
                print(f"Способность {ability.__name__} не найдена!")
        # Если передается экземпляр способности
        else:
            # Проверяем есть ли способность такого типа в списке
            ability_instance = next(
                (a for a in self._abilities if isinstance(a, ability.__class__)), None
            )
            if ability_instance:
                ability_instance.use(self, target)
            else:
                print(f"Способность {ability.name} не найдена!")

    def use_random_ability(self, target: ICharacter) -> None:
        if not self._abilities:
            self.attack(target)
            return

        ability = random.choice(self._abilities)
        ability.use(self, target)

    @property
    def abilities(self) -> List[IAbility]:
        return self._abilities

    # Статистика

    def show_status(self):
        """Выводит основную информацию о персонаже"""
        print(f"\n=== Статус {self.name} ===")
        print(f"Здоровье: {self._health}/{self.MAX_HEALTH}")
        print(
            f"Сила: {self._stats.strength} Ловкость: {self._stats.agility} Интеллект: {self._stats.intelligence}"
        )

        # Информация об оружии
        if self._weapon:
            print(
                f"Выбранное оружие: {self._weapon.name} (Урон: {self._weapon.damage})"
            )
        else:
            print("Оружие: нет")

        # Информация о способностях
        print("\nСпособности:")
        if not self._abilities:
            print("  Нет доступных способностей")
        else:
            for i, ability in enumerate(self._abilities, 1):
                print(f"  {i}. {ability.name}")

        # Информация о расходниках
        print("\nИнвентарь:")
        if not self._consumables:
            print("  Пусто")
        else:
            for item, items in self._consumables.items():
                print(f"  {item.__name__}: {len(items)} шт.")

        # Активные баффы
        if self._active_buffs:
            print("\nАктивные эффекты:")
            for buff, value in self._active_buffs.items():
                print(f"  {buff}: +{value}")
        print("\n")
