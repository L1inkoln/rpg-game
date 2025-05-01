from abilities.abilities import DoubleShot, Fireball, PowerStrike
from characters.base import ICharacter
from characters.classes.archer import Archer
from characters.classes.mage import Mage
from characters.classes.warrior import Warrior
from items.arrows import Arrow, FireArrow, FrostArrow
from items.potions import HealthPotion
from items.weapons import Bow, Staff, Sword


# Фабрика для создания классов можно настроить снаряжение и оружие
class CharacterFactory:
    @staticmethod
    def create_mage(name: str) -> "ICharacter":
        mage = Mage(name)
        mage._add_ability(Fireball())
        mage.equip_weapon(Staff())
        return mage

    @staticmethod
    def create_archer(name: str) -> "ICharacter":
        archer = Archer(name)
        archer._add_ability(DoubleShot())
        archer.equip_weapon(Bow())
        archer._add_consumable(Arrow())
        archer._add_consumable(FireArrow())
        archer._add_consumable(FrostArrow())
        return archer

    @staticmethod
    def create_warrior(name: str) -> "ICharacter":
        warrior = Warrior(name)
        warrior._add_ability(PowerStrike())
        warrior.equip_weapon(Sword())
        warrior._add_consumable(HealthPotion())

        return warrior
