import random
from typing import Optional, Type, Union
from abilities.base import IAbility
from characters.base import ICharacter, Stats
from characters.character import Character
from items.weapons import Staff, Weapon
from levels.level import IEnemy


class Mage(Character):
    def __init__(self, name: str):
        self.MAX_HEALTH = 50
        super().__init__(name, Stats(strength=8, agility=8, intelligence=14))
        self._is_casting = False  # Флаг для защиты от рекурсии

    def attack(
        self,
        target: Union[ICharacter, IEnemy],
        ability: Optional[Union[IAbility, Type[IAbility]]] = None,
    ) -> None:
        # Если уже в процессе каста, используем обычную атаку
        if self._is_casting:
            return super().attack(target)

        # Проверка наличия посоха
        if not isinstance(self._weapon, Staff):
            print(f"{self.name} не может кастовать без посоха!")
            return super().attack(target)

        # Проверка наличия способностей
        if not self._abilities:
            print(f"У {self.name} нет изученных заклинаний")
            return super().attack(target)

        # Логика выбора заклинания
        if ability is None and len(self.abilities) > 0:
            # Случайное заклинание, если не указано конкретное
            ability_to_use = random.choice(self._abilities)
        elif isinstance(ability, type):
            super().use_ability(ability, target)

        # Использование заклинания
        self._is_casting = True
        self.use_ability(ability_to_use, target)
        self._is_casting = False

    def can_equip_weapon(self, weapon: Weapon) -> bool:
        return isinstance(weapon, Staff)
