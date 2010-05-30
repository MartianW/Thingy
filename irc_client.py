"""This module contains the irc client class, which handles the entire IRC interface"""

#This module is very comment heavy. I blame it on the crypticness of the IRC protocol

from socket import socket #For connecting to the IRC server

#Configuration. Later this might be moved to a settings module
nick = 'Thingy_v1_0'
password = 'oA,"2!'
owner = 'Martin'
server = 'irc.foonetic.net'
port = 6667
channel = '#Thingy'
rawlog = False
modeValues = {'+': 1, '%': 2, '@': 3, '&':4}

class IRC_Client:
	"""IRC stuff. Initialization takes a Thingy object, which it calls with relevant events"""
	def __init__(self, interface):
                self.interface = interface
		self.socket = socket() #Socket class
		self.socket.connect((server, port)) #Connect
                self.running = True
		self.namesResult = [] #Used for buffering information returned from names request
                self.modes = {} #Dictionary for storing users and their modes
                
		print "Connecting to the server..."
		#Next two lines are required by IRC protocol to be first thing sent
		self.send('NICK %s' % nick) #Choose nickname
		self.send('USER %s * * :A bot of %s.' % (owner, owner)) #choose user name.
        
        @property
        def bot(self):
                return self.interface.bot
        
	def send(self, msg):
		"""For sending a message to the IRC server. Attaches \r\n and prints debugging info."""
		if rawlog: print '=> %s' % msg.rstrip()
		self.socket.send(msg + '\r\n')
		
	def join(self, chan):
		"""Join a channel"""
		self.send('JOIN ' + chan)
	
	def loop(self):
		"""Main loop for handling input from the socket. Thread blocking."""
		readbuffer = ''
		while self.running:
			readbuffer = readbuffer + self.socket.recv(1024) #Top up the buffer
			temp = readbuffer.split("\n")
			readbuffer = temp.pop( ) #The last line is possibly half read

			for rawl in temp:
				rawl = rawl.rstrip() #Remove trailing \r\n
				if rawlog: print "<= " + rawl
				line = rawl.split(" ") #Split for easier parsing
                                
				#Respond to pings
				if line[0] == "PING": #IRC server pings in the format PING :<data>
					self.send("PONG " + line[1]) #Reply PONG :<data>
	
				#Once connected, do stuff
				elif line[1] == "001": #IRC server signals welcome message in format <server> 001 <nick> <msg> 
					self.send("MODE " + nick + " +B") #Mark ourselves as a bot
					self.send("PRIVMSG NICKSERV IDENTIFY " + password) #Identify with Nickserv
					print "Connected to the server."
	
				#We've received a notice from nickserv
				elif (line[0].startswith(":NickServ") and line[1] == "NOTICE" and line[2] == nick):
					if (' '.join(line[3:]) == ":Password accepted -- you are now recognized."): #We're logged in
						print "Identified with NickServ, now joining main channel."
						self.join(channel)
				
				#We've received a message in a channel or pm. (PRIVMSG is for channels as well.)
				elif line[1] == "PRIVMSG": #Messages are of the form nick!username@machine.domain.tld PRIVMSG <channel> :<msg>
					if line[2] == nick: #The message is sent via pm if <channel> is equal to nick
						private = True #It's a private message
					else:
						private = False #It was said in a channel
					sender = line[0].split("!")[0][1:] #Extract the sender's nick
					msg = ' '.join(line[3:])[1:] #Patch together the actual message from the list of words
                                        try:
                                                mode = self.modes[sender]
                                                self.bot.msg(sender, msg, private, mode) #Pass the message along
                                        except KeyError: #If the user isn't in the channel and therefore not in modes, ignore him. This will hopefully prevent abuse
                                                pass
                                        
                                elif (line[1] == "JOIN") and (line[0].split("!", 1)[0] != ':' + nick): #A user joined. Second bit is to check that it isn't the bot joining the channel (in which case, the server automatically sends a names list without a request)
                                        self.refreshMembers() #Refresh the memberlist
                                        print "A user joined"
                                
                                elif line[1] == "PART": #A user parted.
                                        self.refreshMembers()
                                        print "A user parted"
                                        
                                elif line[1] == "KICK": #A user was kicked
                                        self.refreshMembers()
                                        print "A user was kicked"
                                        
                                elif line[1] == "QUIT": #A user quit
                                        self.refreshMembers()
                                        print "A user quit"
                                        
                                elif line[1] == "NICK": #A user changed their nick
                                        self.refreshMembers()
                                        print "A user changed their nick"
                                        
                                elif (line[1] == "MODE") and (line[2] == channel): #A user's mode was changed. line[2] must equal channel, otherwise thingy twigs on setting itself +B
                                        self.refreshMembers()
                                        print "A user's mode was changed"
                                
                                elif line[1] == "353": #A partial or full list of names in the channel
                                        line[5] = line[5][1:] #Chopping off : in front of first name
                                        self.namesResult.extend(line[5:]) #Names start at the sixth word
                                        
                                elif line[1] == "366": #Indicates end of sending names
                                        for name in self.namesResult:
                                                if name[0] in modeValues:
                                                        self.modes[name[1:]] = modeValues[name[0]] #get number for each mode
                                                else:
                                                        self.modes[name] = 0 #No mode
                                        self.namesResult = [] #Clear the buffer
                                        print "Modes reloaded:"
                                        for user in self.modes:
                                                print "%s: level %s." % (user, self.modes[user])
                                        
        def refreshMembers(self):
                """Requests a new memberlist from the server"""
                self.send("NAMES %s" % channel)
                                
        def end(self):
                self.socket.close()

        def announce(self, msg): #Announce something to every channel the bot is in
                self.sayTo(msg, channel) #For now the bot is always in one channel, but later this may change. E.g. dead players lounge

        def sayTo(self, msg, target): #Say something to a specific person
                self.send("PRIVMSG %s %s" % (target, msg))
        
if __name__ == "__main__":
	class Test:
		def msg(self, sender, msg, private):
			print sender, msg, private

	i = IRC_Client(Test())
	i.loop()
