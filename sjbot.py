import irc
import commands
import socket
import sys
import time
import imp
import os

print( sys.version )
print("Bot started. Thank you for using Uptone Software!")

try:
	passFile		= os.path.dirname(os.path.realpath(__file__)) + "/password"
except:
	passFile 		= "password"

class sjBot():
	
	#== Variables
	botName 	= "sjBots"
	botCmd 		= ["`", botName + ",", botName + ":" ]
	network 	= "irc.freenode.net"
	port 		= 6667
	channelList 	= ["#Sjc_Bot"]
	#============

	password 	= open(passFile, 'r').read()

	def __init__(self, commands):
		self.irc 		= irc._irc(self.network, self.port)
		self.commands 		= commands._commands(self.irc, self.botCmd)
		print("Commands module imported.")
		self.irc.joinserver(self.botName)
		self.irc.login(self.password)
		self.irc.waitUntil("396 " + self.botName, 10)
		self.irc.join( self.channelList )
		self.loop( commands)


	def loop(self, commands):
		recData 	= 1

		while recData:


			oldCommands 		= commands
			try:
				commands 		= imp.reload( commands )
				self.commands 		= commands._commands(self.irc, self.botCmd)
			except:
				commands 		= oldCommands
				self.commands		= commands._commands(self.irc, self.botCmd )


			recData 	= self.irc.recv(1)
			

			if recData == "__continue__":
				continue

			splitData 	= recData.split(" ")
			splitData[-1]	= str( splitData[-1] )[:-2]


			if splitData[0] == "PING":
				self.irc.pong( splitData[1][1:] )


			if len( splitData ) >= 3 and splitData[1] == "PRIVMSG":
				for btcmd in self.botCmd:
					if btcmd in splitData[3]:

						try:
							user 			= splitData[0].split("!")[0]
							user 			= user[1:]
							host 			= splitData[0].split("!")[1]
						except IndexError:
							continue


						msgtype 		= splitData[1]
						channel 		= splitData[2]
				

						try:
							if self.botName in btcmd:
								command 	= splitData[4].lower()
								params 		= splitData[5:]
							else:
								command 		= splitData[3]
								command 		= command[len(btcmd)+1:].lower()
								params 			= splitData[4:]
						except IndexError:
							continue

						print( command )
						print( params )
					
						if len( command ) == 0:
							continue

						if channel == self.botName:
							channel 	= user

						commandParams		= [command, user, host, channel, params ]
						self.commands.callCommand( commandParams )
						break


if __name__ == "__main__":
	sjBot 		= sjBot(commands)
