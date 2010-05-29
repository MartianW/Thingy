#from game import Game
#from game import C9RoleFact #Todo: Possibly import from separate setups module in future

class ThingyError(Exception):
    "raised whenever something happens that thingy can't handle."
    
class Manual_Action(Exception):
    "raised for actions that have no handler"
    
class Thingy(object):
        def __init__(self, interface):
                self.interface = interface
                self.game = None
                self.test = False
                
        @property
        def client(self):
                return self.interface.client
        
        def msg(self, sender, msg, private):
                if msg[0] == "!": #It starts with an exclamation mark, so it's a command
                        line = msg.split(" ") #Split for easier parsing
                        action = line[0][1:] #Trimming the !
                        args = line[1:]
                        if (self.game != None): #If a game object exists, the command must be for it
                                #self.game.action(action, args) #Pass it along
                                pass
                        elif action == "start":
                                if (args[0].lower() == "c9"): #Todo: Replace with dictionary of setups and names
                                        #self.game = Game(C9RoleFact)
                                        self.players = []
                                        self.say("Signups starting for a C9 game")
                                        for player in args[1:]: #Players may be optionally signed with !start <setup> [<player> <player>]
                                                self.players.append(player)
                                                self.sayTo("Confirming your sign-up for the C9 game.", player)
                        elif action == "reload": #Work out some kind of permission system later
                                if args[0] == "Thingy":
                                        self.interface.reloadThingy()
                                elif args[0] == "Client":
                                        self.test = True
                                        self.interface.reloadClient()
                        elif action == "test": #For testing if Thingy keeps its state between reloads"
                                if self.test:
                                        self.say("Success!")
                                else:
                                        self.say("Failure!")
                                       
        def say(self, msg): #Say to everyone
                self.client.announce(msg)
                
        def sayTo(self, msg, target): #Say to a specific person
                self.client.sayTo(msg, target)
                
        def  __del__(self):
                print "Thingy out."

if __name__ == "__main__":
        Thingy()