from __future__ import annotations
from typing import Dict, List, Type
from abilities.base import IAbility
from characters.base import ICharacter, Stats
from items.base import IConsumable


class Character(ICharacter):
    MAX_HEALTH = 100

    def __init__(self, name: str, stats: Stats):
        self._name = name
        self._stats = stats
        self._health = self.MAX_HEALTH
        self._weapon = None
        self._consumables: Dict[Type[IConsumable], List[IConsumable]] = {}
        self._abilities: List[IAbility] = []
        self._active_buffs: Dict[str, int] = {}

    # Базовые свойства
    @property
    def name(self) -> str:
        return self._name

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
        self._health = min(self.MAX_HEALTH, self._health + amount)
        print(f"{self.name} восстановил {amount} HP!")

    def equip_weapon(self, weapon) -> bool:
        if not weapon.can_equip(self):
            print(f"{self.name} не может использовать {weapon.name}!")
            return False

        self._weapon = weapon
        print(f"{self.name} экипировал {weapon.name}!")
        return True

    def attack(self, target: ICharacter) -> None:
        damage = self._calculate_damage()
        if self._weapon:
            print(
                f"{self.name} атакует {target.name} {self._weapon.name}! (Урон: {damage})"
            )
            self._weapon.apply_damage(target, damage)
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
    def add_consumable(self, item: IConsumable) -> None:
        item_type = type(item)
        if item_type not in self._consumables:
            self._consumables[item_type] = []

        if len(self._consumables[item_type]) < item.max_stack:
            self._consumables[item_type].append(item)
            print(f"Добавлен предмет: {item.name}")
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
            print(f"Урон увеличен на {effects['damage_buff']} на 3 хода!")

    def get_consumable_count(self, item_type: Type[IConsumable]) -> int:
        return len(self._consumables.get(item_type, []))

    # Система способностей
    def add_ability(self, ability: IAbility) -> None:
        self._abilities.append(ability)
        print(f"Добавлена способность: {ability.name}")

    def use_ability(self, index: int, target: ICharacter) -> None:
        if 0 <= index < len(self._abilities):
            self._abilities[index].use(self, target)
        else:
            print(f"Способность #{index} не найдена!")

    # Статистика
    def show_status(self) -> None:
        """Выводит основную информацию о персонаже"""
        print(f"\n=== Статус {self.name} ===")
        print(f"Здоровье: {self._health}/{self.MAX_HEALTH}")
        print(
            f"Сила: {self._stats.strength} Ловкость: {self._stats.agility} Интеллект: {self._stats.intelligence}"
        )

        # Информация об оружии
        if self._weapon:
            print(f"Оружие: {self._weapon.name} (Урон: {self._weapon.damage})")
        else:
            print("Оружие: нет")

        # Информация о расходниках
        print("\nИнвентарь:")
        if not self._consumables:
            print("  Пусто")
        else:
            for item_type, items in self._consumables.items():
                print(f"  {item_type.__name__}: {len(items)} шт.")

        # Активные баффы
        if self._active_buffs:
            print("\nАктивные эффекты:")
            for buff, value in self._active_buffs.items():
                print(f"  {buff}: +{value}")
