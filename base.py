from irc_client import IRC_Client
from game import Game
from game import C9RoleFact #Todo: Possibly import from separate setups module in future

class ThingyError(Exception):
    "raised whenever something happens that thingy can't handle."
    
class Manual_Action(Exception):
    "raised for actions that have no handler"
    
class Thingy(object):
        def __init__(self):
                self.irc = IRC_Client(self)
                self.irc.loop()
                self.game = None
                
        def msg(self, sender, msg, private):
                self.say("Hello.")
                if msg[0] == "!": #It starts with an exclamation mark, so it's a command
                        line = msg.split(" ") #Split for easier parsing
                        action = line[0][:1] #Trimming the !
                        args = line[1:]
                        if (self.game != None): #If a game object exists, the command must be for it
                                self.game.action(action, args) #Pass it along
                        elif action == "start":
                                if (args[0].lower == "c9"): #Todo: Replace with dictionary of setups and names
                                        self.game = Game(C9RoleFact)
                                        
        def say(self, msg): #Say to everyone
                self.irc.announce(msg)
                
        def sayTo(self, msg, target): #Say to a specific person
                self.irc.sayTo(msg, target)

if __name__ == "__main__":
        Thingy()