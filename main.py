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
 
npc1 = NPC('Hog Rider')

npc2 = NPC('Hog Rider 2')

hero.go_in_castle()
hero.go_outside()
hero.healing(dragon1)
hero.attack_with_dragon(npc1, dragon1)
hero.attack_with_skeleton(npc2, skelet1)
hero.check_hero_statistics(dragon1, skelet1)
