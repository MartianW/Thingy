"""Game_starter:
!C9
!cancel
!join


Everyone:
!vote
!unvote

Night Actions:
!mafia_kill
!doctor
!cop
"""
import random
from Roles import *

class C9:
	def __init__(self, players):
		random.shuffle(players)
		rolelist = [Townie, Townie, Townie, Mafia, Mafia] + random.choice([[Townie, Townie], [Townie, Cop], [Doctor, Townie], [Doctor, Cop]])
		roles = {}
		for p in players:
			roles[p] = rolelist.pop()(p)

Players = ["P1", "P2", "P3", "P4", "P5", "P6", "P7"]
c = C9(Players)
