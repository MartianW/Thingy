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

class IRC_Client:
	"""IRC stuff. Initialization takes a Thingy object, which it calls with relevant events"""
	def __init__(self, bot):
		self.bot = bot
		self.socket = socket() #Socket class
		self.socket.connect((server, port)) #Connect
		
		#Next two lines are required by IRC protocol to be first thing sent
		self.send('NICK %s' % nick) #Choose nickname
		self.send('USER %s * * :A bot of %s.' % (nick, owner)) #choose user name.
		
	def send(self, msg):
		"""For sending a message to the IRC server. Attaches \r\n and prints debugging info."""
		print '=> %s' % msg.rstrip()
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
				print "<= " + rawl
				line = rawl.split(" ") #Split for easier parsing
				
				#Respond to pings
				if line[0] == "PING": #IRC server pings in the format PING :<data>
					self.send("PONG " + line[1]) #Reply PONG :<data>
	
				#Once connected, do stuff
				elif line[1] == "376": #IRC server signals end of MoTD in format <server> 367 <nick> <msg> 
					self.send("MODE " + nick + " +B") #Mark ourselves as a bot
					self.send("PRIVMSG NICKSERV IDENTIFY " + password) #Identify with Nickserv
	
				#We've received a notice from nickserv
				elif (line[0].startswith(":NickServ") and line[1] == "NOTICE" and line[2] == nick):
					if (' '.join(line[3:]) == ":Password accepted -- you are now recognized."): #We're logged in
						self.join(channel)
				
				#We've received a message in a channel or pm. (PRIVMSG is for channels as well.)
				elif line[1] == "PRIVMSG": #Messages are of the form nick!username@machine.domain.tld PRIVMSG <channel> :<msg>
					if line[2] == nick: #The message is sent via pm if <channel> is equal to nick
						private = True #It's a private message
					else:
						private = False #It was said in a channel
					sender = line[0].split("!")[0] #Extract the sender's nick
					msg = line[3][1:] #Extract the actual message
					self.bot.msg(sender, msg, private) #Pass the message along