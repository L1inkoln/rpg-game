from characters.base import ICharacter, Stats
from characters.character import Character
from typing import Optional, Type, cast
from items.arrows import Arrow
from items.weapons import Bow, Knife, Weapon
from levels.level import IEnemy


class Archer(Character):
    def __init__(self, name: str):
        self.MAX_HEALTH = 70
        super().__init__(name, Stats(strength=10, agility=18, intelligence=10))

    def attack(
        self, target: ICharacter | IEnemy, arrow_type: Optional[Type[Arrow]] = None
    ) -> None:
        if not isinstance(self._weapon, Bow):
            print(f"{self.name} не может стрелять без лука!")
            super().attack(target)
            return

        arrow = self._get_arrow(arrow_type)
        if arrow is None:
            print("Нет выбранной стрелы в инвентаре!")
            super().attack(target)
            return

        damage = self._calculate_arrow_damage(arrow)
        print(f"{self.name} стреляет {arrow.name} в {target.name}! (Урон: {damage})")
        arrow.apply_effect(target)
        target.take_damage(damage)

        print(f"({arrow.name}: осталось {self.get_consumable_count(type(arrow))})")

    def _get_arrow(self, arrow_type: Optional[Type[Arrow]]) -> Optional[Arrow]:
        """Ищет стрелу в инвентаре и удаляет её"""
        if arrow_type is None:
            # Ищем любую стрелу
            for items in list(self._consumables.values()):
                for i, item in enumerate(items):
                    if isinstance(item, Arrow):
                        return cast(Arrow, self._consumables[type(item)].pop(i))
        # если явно указан тип стрелы
        elif arrow_type in self._consumables:
            for i, item in enumerate(self._consumables[arrow_type]):
                if isinstance(item, Arrow):
                    return cast(Arrow, self._consumables[arrow_type].pop(i))
        return None

    def _calculate_arrow_damage(self, arrow: Arrow) -> int:
        return arrow.damage + (self._weapon.damage if self._weapon else 0)

    def can_equip_weapon(self, weapon: Weapon) -> bool:
        return isinstance(weapon, Bow | Knife)
