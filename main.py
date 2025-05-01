from levels.castle import CastleLevel
from levels.dungeon import DungeonLevel
from factories import CharacterFactory


# Простой уровень со скелетами
def dungeon_level():
    dungeon = DungeonLevel()
    warrior = CharacterFactory.create_warrior("Гатс")
    dungeon.start(heroes=[warrior])
    warrior.show_status()


# Уровень с боссом
def boss_level():
    castle = CastleLevel()
    archer = CharacterFactory.create_archer("Лучник")
    mage = CharacterFactory.create_mage("Маг")
    warrior = CharacterFactory.create_warrior("Гатс")
    castle.start(heroes=[archer, mage, warrior])


if __name__ == "__main__":
    # dungeon_level()
    boss_level()
