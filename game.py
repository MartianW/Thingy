"""
Actions this will hopefully support soon:
Pregame:
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
from base import *
from roles import *

from random import choice, shuffle
from itertools import imap, izip

def C9RoleFact():
	baseRoles = [Townie, Townie, Townie, Mafia, Mafia]
	randomRoles = [[Townie, Townie],
		   [Townie, Cop],
		   [Doctor, Townie],
		   [Doctor, Cop]]
	return iter(baseRoles + random.choice(randomRoles))

class Game:
	"""vanilla c9 game by default. When we add more games later we might
	want to change this into an abstract base class and/or add the option
	for passing a setup to the Game class"""

	def __init__(self, players, roles=C9RoleFact):
		"""Constructor. Starts the game at D1 and is initialized with
		the player list"""
		random.shuffle(players)
		
		try:
			rolelist = roles()
		except TypeError:
			rolelist = roles
		
		self.roles = dict((player, role(player)) for player, rolelist in izip(players, rolelist))
		
	def action(self, player, action, args):
		"""Whenever a player does an action, it's passed to his role.
		This includes votes."""
		try:
			act = getattr(self.roles[player],"action_%s(args)" % action,None)  #TODO: Convert give the Role class some means to convert the string aruments into players/Roles
		except KeyError: #The person who did the action is not a player. Ignore him.
			pass
		if act is None: #There exists no such action for that player. Inform the mod if there is one, and continue
			raise Manual_Action("%s %ss %s" % (player, action, ' '.join(args)))
		act()
if __name__ == "__main__":
	print "Running test of Game.py"
	Players = ["P1", "P2", "P3", "P4", "P5", "P6", "P7"]
	c9 = Game(Players)
	print c9.roles
	c9.action("P1", "vote", ["P2"])
