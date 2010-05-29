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
rawlog = True

class IRC_Client:
	"""IRC stuff. Initialization takes a Thingy object, which it calls with relevant events"""
	def __init__(self, bot):		
		self.bot = bot
		self.socket = socket() #Socket class
		self.socket.connect((server, port)) #Connect
		
		print "Connecting to the server..."
		#Next two lines are required by IRC protocol to be first thing sent
		self.send('NICK %s' % nick) #Choose nickname
		self.send('USER %s * * :A bot of %s.' % (owner, owner)) #choose user name.

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
		while True:
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
					msg = ' '.join(line[3:])[1:] #Extract the actual message
					self.bot.msg(sender, msg, private) #Pass the message along

        def announce(self, msg): #Announce something to every channel the bot is in
                self.sayTo(self, msg, channel) #For now the bot is always in one channel, but later this may change. E.g. dead players lounge

        def sayTo(self, msg, target): #Say something to a specific person
                self.send("PRIVMSG %s %s" % (target, msg))
        
if __name__ == "__main__":
	class Test:
		def msg(self, sender, msg, private):
			print sender, msg, private

	i = IRC_Client(Test())
	i.loop()
