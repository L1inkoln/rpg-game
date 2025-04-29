from abilities.base import IAbility
from typing import TYPE_CHECKING, Union

from characters.character import Character
from items.arrows import Arrow
from items.weapons import Bow
from levels.level import IEnemy

if TYPE_CHECKING:
    from characters.base import ICharacter
    from items.arrows import Arrow
    from abilities.base import IAbility


class PowerStrike(IAbility):
    @property
    def name(self) -> str:
        return "Мощный удар"

    def use(self, caster: "ICharacter", target: "ICharacter") -> None:
        damage = caster.stats.strength + 10
        print(f"{caster.name} использует {self.name} и наносит {damage} урона!")
        target.take_damage(damage)


class DoubleShot(IAbility):
    @property
    def name(self) -> str:
        return "Двойной выстрел"

    def use(self, caster: Character, target: Character) -> None:
        if not isinstance(caster._weapon, Bow):  # Проверка наличия метода
            print(f"{caster.name} не может применить способность без лука!")
            caster.attack(target)
            return

        # Использование способности если есть две стрелы
        if caster.get_consumable_count(Arrow) >= 2:

            # Красивый вывод об использовании способности
            message = f"{caster.name} использует {self.name}!"
            width = len(message) + 2
            print("\n" + "╔" + "═" * width + "╗")
            print("║ " + message + " ║")
            print("╚" + "═" * width + "╝")

            print("\n▶ Первый выстрел:")
            caster.attack(target)
            print("\n﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌")
            print("▶ Второй выстрел:")
            caster.attack(target)
            # Итоговый разделитель
            print("▁" * 40)
        else:
            print(
                f"Сработала способность '{self.name}', но нехватает стрел. Используется обычная атка"
            )
            caster.attack(target)


# class Heal(IAbility):
#     @property
#     def name(self) -> str:
#         return "Лечение"

#     def use(self, caster: "ICharacter", target: "ICharacter") -> None:
#         heal_amount = 25
#         print(f"{caster.name} исцеляет {target.name} на {heal_amount} HP!")
#         target.heal(heal_amount)  # Теперь heal доступен


class Fireball(IAbility):
    @property
    def name(self) -> str:
        return "Огненный шар"

    def use(self, caster: "ICharacter", target: Union["ICharacter", "IEnemy"]) -> None:
        damage = caster.stats.intelligence * 2
        print(f"{caster.name} использует {self.name} и наносит {damage} урона!")
        target.take_damage(damage)
