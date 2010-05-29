import base
import irc_client

class ThingyIRCInterface():
    """An interface between Thingy and the IRC_Client, so that they don't have to know about each other and can thingyh be reloaded independently.
    (Reloading the IRC Client would reset the connection, but not lose the game info, while reloading thingy does the opposite)"""
    def __init__(self):
        self.irc = irc_client.IRC_Client(self)
        self.thingy = base.Thingy(self)
        
    def reloadThingy(self):
        print "Reloading thingy"
        reload(base)
        self.thingy = base.Thingy(self)
        
    def reloadClient(self):
        print "Reloading IRC_Client"
        reload(irc_client)
        self.irc.running = False
        self.irc.end()
        self.irc = irc_client.IRC_Client(self)
        
    def run(self):
        while True:
            self.irc.loop()

    #Making the names more general
    @property
    def bot(self):
        return self.thingy
        
    @property
    def client(self):
        return self.irc

thingy = ThingyIRCInterface()
thingy.run()