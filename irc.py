import socket
import time

class _irc():
	
	def __init__(self, network, port):
		self.irc 		= socket.socket( socket.AF_INET, socket.SOCK_STREAM )
		self.irc.connect((network, port))
		self.channelList 	= []

	def joinserver(self, botName ):
		botName		= bytes( botName, 'utf-8' )
		self.botName 	= botName
		self.irc.send(b"NICK " + botName + b" \r\n")
		self.irc.send(b"USER " + botName + b" " + botName + b" " + botName + b" :Uptone Software\r\n")
		return 0


	def nick(self, botName ):
		self.irc.send(b"NICK " + bytes(botName, 'utf-8' ) + b" \r\n")
		return 0

	def login(self, password):
		self.irc.send(b"PRIVMSG NickServ :Identify " + self.botName + b" " + password.encode('utf-8') + b"\r\n")
		return 0


	def pong(self, server ):
		self.irc.send(b"PONG " + bytes( server, "utf-8" ) + b"\r\n")
		return 0


	def join(self, channels ):
		for k in channels:
			self.channelList.append( k )
			self.irc.send(b"JOIN " + bytes( k, 'utf-8' ) + b"\r\n")
		return 0


	def leave(self, channels ):
		for k in channels:
			self.channelList.remove( k )
			self.irc.send(b"PART " + bytes( k, 'utf-8' ) + b"\r\n")
		return 0


	def pMessage(self, toWho, message ):
		if toWho == "__all__":
			for x in self.channelList:
				self.pMessage( x, message )	
				return 0

		if isinstance(toWho, list ):
			for ch in toWho:
				if ch in self.channelList:
					self.pMessage( ch, message )

		try:
			if isinstance(message, str):
				self.irc.send(b"PRIVMSG " + bytes( toWho, "utf-8") + b" :" + bytes( message, "utf-8") + b"\r\n")
			else:
				for k in message:
					self.irc.send(b"PRIVMSG " + bytes( toWho, "utf-8") + b" :" + bytes( k, "utf-8") + b"\r\n")
					time.sleep(0.5)
		except TypeError:
			return 1
		return 0

	def notice(self, toWho, message ):
		print( "NOTICE")
		return 0

	
	def recv(self, log=0, ammount=1024):
		try:
			recievedData 		= self.irc.recv(ammount ).decode('utf-8')
		except UnicodeDecodeError:
			print("Jank characters caught!")
			return "__continue__"
		if log:
			print( recievedData )
		return recievedData
