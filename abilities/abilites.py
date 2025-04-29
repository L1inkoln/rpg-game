from abilities.base import IAbility
from typing import TYPE_CHECKING, Union
from items.arrows import Arrow
from items.weapons import Bow
from levels.base import IEnemy

if TYPE_CHECKING:
    from characters.base import ICharacter
    from items.arrows import Arrow
    from abilities.base import IAbility


class PowerStrike(IAbility):
    @property
    def name(self) -> str:
        return "Мощный удар"

    def use(self, caster, target) -> None:
        damage = caster._calculate_damage() + 10
        print(f"{caster.name} использует {self.name} и наносит {damage} урона!")
        target.take_damage(damage)


class DoubleShot(IAbility):
    @property
    def name(self) -> str:
        return "Двойной выстрел"

    def use(self, caster, target) -> None:
        if not isinstance(caster._weapon, Bow):  # Проверка наличия метода
            print(f"{caster.name} не может применить способность без лука!")
            caster.attack(target)
            return

        # Использование способности если есть две стрелы
        if caster.get_consumable_count(Arrow) >= 2:

            # Красивый вывод об использовании способности
            print(f"{caster.name} использует {self.name}!")
            print("\n▶ Первый выстрел:")
            caster.attack(target)
            print("\n﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌﹌")
            print("▶ Второй выстрел:")
            caster.attack(target)
            print("▁" * 40)
        else:
            print(
                f"Сработала способность '{self.name}', но нехватает стрел. Используется обычная атка"
            )
            caster.attack(target)


class Fireball(IAbility):
    @property
    def name(self):
        return f"{'\033[38;5;208m'}Огненный шар{'\033[0m'}"

    def use(self, caster: "ICharacter", target: Union["ICharacter", "IEnemy"]) -> None:
        damage = caster.stats.intelligence * 2
        print(f"{caster.name} использует {self.name} и наносит {damage} урона!")
        target.take_damage(damage)
