from abilities.base import IAbility
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from characters.base import ICharacter


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

    def use(self, caster: "ICharacter", target: "ICharacter") -> None:
        if not hasattr(caster, "shoot"):  # Проверка наличия метода
            print(f"{caster.name} не может стрелять!")
            return

        print(f"{caster.name} использует {self.name}:")
        caster.shoot(target)  # type: ignore  # Игнорируем проверку для специализированных классов
        caster.shoot(target)  # type: ignore


class Heal(IAbility):
    @property
    def name(self) -> str:
        return "Лечение"

    def use(self, caster: "ICharacter", target: "ICharacter") -> None:
        heal_amount = 25
        print(f"{caster.name} исцеляет {target.name} на {heal_amount} HP!")
        target.heal(heal_amount)  # Теперь heal доступен
