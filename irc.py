import socket
import time

class _irc():
	
	def __init__(self):
		print( "IRC module imported." )
		self.irc 	= socket.socket( socket.AF_INET, socket.SOCK_STREAM )


	def joinserver(self, network, port, botName ):
		self.irc.connect((network, port))
		botName		= bytes( botName, 'utf-8' )
		self.botName 	= botName
		self.irc.send(b"NICK " + botName + b" \r\n")
		self.irc.send(b"USER " + botName + b" " + botName + b" " + botName + b" :Uptone Software\r\n")
		return 0

	def waitUntil(self, untilText ):
		checkText 		= ""

		while( untilText not in checkText ):
			checkText 	= self.recv(1)
		
		return 0


	def login(self, password):
		print("Login.")
		self.irc.send(b"PRIVMSG NickServ :Identify " + self.botName + b" " + password.encode('utf-8') + b"\r\n")
		return 0


	def pong(self, server ):
		self.irc.send(b"PONG " + bytes( server, "utf-8" ) + b"\r\n")
		return 0


	def join(self, channels ):
		for k in channels:
			self.irc.send(b"JOIN " + bytes( k, 'utf-8' ) + b"\r\n")
		return 0


	def leave(self, channels ):
		for k in channels:
			self.irc.send(b"PART " + bytes( k, 'utf-8' ) + b"\r\n")
		return 0


	def pMessage(self, toWho, message ):

		if isinstance(message, str):
			self.irc.send(b"PRIVMSG " + bytes( toWho, "utf-8") + b" :" + bytes( message, "utf-8") + b"\r\n")
		else:
			for k in message:
				self.irc.send(b"PRIVMSG " + bytes( toWho, "utf-8") + b" :" + bytes( k, "utf-8") + b"\r\n")
				time.sleep(0.5)
		return 0

	def whoIs(self, user ):
		self.irc.send(b"WHOIS " + bytes( user, "utf-8" ) + b"\r\n")
		return self.irc.recv(1024)
	
	def recv(self, log=0, ammount=1024):
		try:
			recievedData 		= self.irc.recv(ammount ).decode('utf-8')
		except UnicodeDecodeError:
			print("Jank characters caught!")
			return "__continue__"
		if log:
			print( recievedData )
		return recievedData
