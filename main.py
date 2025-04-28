from characters.base import Stats
from characters.character import Character
from characters.classes.archer import Archer
from items.arrows import FireArrow, FrostArrow
from items.weapons import Bow, Dagger
from items.potions import HealthPotion
from abilities.abilites import DoubleShot
from levels.dungeon import DungeonLevel


class Enemy(Character):
    def __init__(self, name: str = "Гоблин"):
        super().__init__(name, Stats(strength=8, agility=6, intelligence=4))
        self.MAX_HEALTH = 100
        self._health = self.MAX_HEALTH


def test_archer(archer: Archer, enemy: Enemy):
    print("\n=== ТЕСТИРОВАНИЕ ЛУЧНИКА ===")
    # 1. Проверка без лука
    print("\n1. Попытка стрельбы без лука:")
    archer.shoot(enemy)

    # 2. Добавляем стрелы (3 штуки)
    print("\n2. Добавляем стрелы:")
    archer.add_consumable(FrostArrow())
    archer.add_consumable(FireArrow())
    archer.add_consumable(FrostArrow())
    # 3. Проверка инвентаря
    print("\n3. Состояние инвентаря:")
    print(f"Ледяных стрел: {archer.get_consumable_count(FrostArrow)}")
    print(f"Огненных стрел: {archer.get_consumable_count(FireArrow)}")

    # 4. Экипируем лук
    print("\n4. Экипируем лук и стреляем c абилкой:")
    archer.equip_weapon(Bow())
    archer.add_ability(DoubleShot())
    archer.use_ability(0, enemy)
    # # 5. Серия выстрелов
    print("\n5. Серия выстрелов:")
    archer.shoot(enemy)
    archer.shoot(enemy, FireArrow)
    archer.shoot(enemy, FireArrow)
    archer.shoot(enemy)

    # 6. Проверка инвентаря после стрельбы
    print("\n6. Инвентарь после стрельбы:")
    print(f"Ледяных стрел: {archer.get_consumable_count(FrostArrow)}")
    print(f"Огненных стрел: {archer.get_consumable_count(FireArrow)}")
    # 7. Попытка стрельбы без стрел
    print("\n7. Стрельба без стрел:")
    archer.shoot(enemy)

    # 8. Тест зелья здоровья
    print("\n8. Использование зелья:")
    enemy.attack(archer)
    enemy.attack(archer)
    enemy.attack(archer)
    enemy.attack(archer)
    print(archer.health)
    archer.add_consumable(HealthPotion())
    archer.use_consumable(HealthPotion)
    print(archer.health)
    # Дополнительный тест с кинжалом
    print("\n=== ТЕСТ С КИНЖАЛОМ ===")
    archer.equip_weapon(Dagger())
    archer.add_consumable(FireArrow())
    archer.shoot(enemy)


def archer_test():
    archer = Archer("Леголас")
    enemy = Enemy()
    test_archer(archer, enemy)


def level():
    archer = Archer("Лучник")
    dungeon = DungeonLevel()
    archer.equip_weapon(Bow())
    dungeon.start(heroes=[archer])


if __name__ == "__main__":
    # archer_test()
    level()
