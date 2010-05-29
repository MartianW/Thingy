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
from collections import defaultdict

def C9RoleFact():
    baseRoles = [Townie, Townie, Townie, Mafia, Mafia]
    randomRoles = [[Townie, Townie],
           [Townie, Cop],
           [Doctor, Townie],
           [Doctor, Cop]]
    return iter(baseRoles + choice(randomRoles))

class Game:
    """vanilla c9 game by default. When we add more games later we might
    want to change this into an abstract base class and/or add the option
    for passing a setup to the Game class"""

    def __init__(self, thingy, players, roles=C9RoleFact):
        """Constructor. Starts the game at D1 and is initialized with
        the player list"""
        
        self.thingy = thingy
        self.vote = LynchVote(self)
        
        shuffle(players)
        
        try:
            rolelist = roles()
        except TypeError:
            rolelist = roles
        
        self.roles = dict((player, role(self, player)) for player, role in izip(players, rolelist))
        
    def action(self, player, action, args):
        """Whenever a player does an action, it's passed to his role.
        This includes votes."""
        try:
            act = getattr(self.roles[player],"action_%s" % action)  #TODO: Convert give the Role class some means to convert the string aruments into players/Roles
        except KeyError: #The person who did the action is not a player. Ignore him.
            pass
        if act is None: #There exists no such action for that player. Inform the mod if there is one, and continue
            raise Manual_Action("%s %ss %s" % (player, action, ' '.join(args)))
        act(args)

class VoteContainer:
    """Simple container holding a count and a list of people who voted that way"""
    def __init__(self):
        self.count = 0
        self.votes = []
    def append(voter):
        """add a vote from voter, with a voting power of count"""
        self.votes.append(voter)
        self.count += voter.votePower
    def remove(voter):
        """remove the vote from voter, with a voting power of count"""
        try:
            self.votes.remove(voter)
            self.count -= voter.votePower
        except ValueError:
            pass
        
    def __str__(self):
        if self.count == 0:
            return "0"
        else:
            pnameGet = lambda p: p.pname
            return "%s (%s)" % (self.count, ", ".join(map(pnameGet, self.votes)))

class VoteBase(object):
    def __init__(self, game):
        self.game = game
        self.votes = defaultdict(VoteContainer)
        self.options = set()
        
    def voteFor(self,voter,candidate):
        """register a vote by voter for candidate"""
        if not candidate in self.options:
            raise ThingyError("Invalid vote")
        self.votes[candidate].append(voter)
        game.say(self.votals())
        self.checkMajority()
            

    def unvote(voter,candidate):
        if not candidate in self.options:
            raise ThingyError("Invalid unvote")
        self.votes[candidate].remove(voter)
        
    def checkMajority(self):
        pass
        
    def votals(self, for_=None):
        if for_ is not None:
            if for_ in self.votes and self.votes[for_].count < 0:
                return "%s: %s" % (for_.pname, self.votes[for_])
            else:
                return "%s has no votes" % for_.pname
        else:
            op = []
            for player, votes in self.votes.iteritems():
                if votes.count:
                    op.append("%s: %s" % (player.pname, votes))
            return " ".join(op)

class LynchVote(VoteBase):
    def __init__(self, game):
        VoteBase.__init__(self, game)
        self.options = set(game.playerList)
        self.options.add("NL")
        self.majority = 1 + len(self.options)/2 #int division ftw
    
    def checkMajority(self):
        for player, votes in self.votes.iteritems():
            if votes.count >= self.majority:
                raise Manual_Action("lynch vote majority reached for %s" % player)

class MafiaKillVote(VoteBase):
    def __init__(self, game):
        VoteBase.__init__(self, game)
        self.options = set(game.playerList)
        self.options.add("NL")
        self.majority = 1 + game.mafiaCount/2 #int division ftw

    def voteFor(self, voter, candidate):
        if 

if __name__ == "__main__":
    print "Running test of Game.py"
    Players = ["P1", "P2", "P3", "P4", "P5", "P6", "P7"]
    c9 = Game(Players)
    print c9.roles
    c9.action("P1", "vote", ["P2"])
