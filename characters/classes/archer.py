from characters.base import ICharacter, Stats
from characters.character import Character
from typing import Optional, Type, cast
from items.arrows import Arrow
from items.base import IConsumable
from items.weapons import Bow


class Archer(Character):
    def __init__(self, name: str):
        super().__init__(name, Stats(strength=12, agility=18, intelligence=10))

    def shoot(
        self, target: ICharacter, arrow_type: Optional[Type[Arrow]] = None
    ) -> None:
        if not isinstance(self._weapon, Bow):
            print(f"{self.name} не может стрелять без лука!")
            self.attack(target)
            return

        arrow = self._get_arrow(arrow_type)
        if arrow is None:
            print("Нет подходящих стрел!")
            self.attack(target)
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
        return (
            arrow.damage
            + (self._stats.agility // 3)
            + (self._weapon.damage if self._weapon else 0)
        )

    def get_consumable_count(self, item_type: Type[IConsumable]) -> int:
        """Переопределяем для правильной типизации"""
        return super().get_consumable_count(item_type)
