import time
from dragon import Dragon
from hero import Hero
from skeleton import Skeleton
from npc import NPC
from player import Player

pl = Player('red', 'Matvey_pro')
hero = Hero('Makanchik')
dragon1 = Dragon('Leviathan')
skelet1 = Skeleton('Varior')
npc =  NPC('Hog Rider')
# hero.attack_with_skeleton()
hero.healing()
# hero.attack_with_dragon()
hero.check_hero_statistics()
