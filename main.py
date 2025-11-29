import time
from dragon import Dragon
from hero import Hero
from skeleton import Skeleton
from npc import NPC
from player import Player

pl = Player('red', 'Matvey_pro')
hero = Hero('Makanchik', 1500, 100)
dragon1 = Dragon('Leviathan', 500, 50, 50)
skelet1 = Skeleton('Varior', 700, 70)
npc =  NPC('Hog Rider', 1500, 60)
hero.attack_with_skeleton()
