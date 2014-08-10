#! /urs/bin/python3
import irc
import commands
import socket
import sys
import time


print( sys.version )
print("Bot started. Thank you for using Uptone Software!")

class sjBot():
	
	#== Variables
	botName 	= "sjBot"
	botCmd 		= "~"
	network 	= "irc.freenode.net"
	port 		= 6667
	channelList 	= ["#Sjc_Bot"]
	#============

	password 	= open('password', 'r').read()

	def __init__(self):
		self.irc 		= irc._irc()
		self.commands 		= commands._commands(self.irc, self.botCmd)
		self.irc.joinserver(self.network, self.port, self.botName)
		self.irc.login(self.password)
		self.irc.waitUntil("396 " + self.botName)
		self.irc.join( self.channelList )
		self.loop()


	def loop(self):
		recData 	= 1

		while recData:
			recData 	= self.irc.recv(1).replace("\r\n", "")
			

			if recData == "__continue__":
				continue

			splitData 	= recData.split(" ")

			if splitData[0] == "PING":
				self.irc.pong( splitData[1][1:] )


			if len( splitData ) >= 3 and splitData[1] == "PRIVMSG":
				if self.botCmd in splitData[3]:

					user 			= splitData[0].split("!")[0]
					user 			= user[1:]
					host 			= splitData[0].split("!")[1]
					msgtype 		= splitData[1]
					channel 		= splitData[2]
					command 		= splitData[3]
					command 		= command[2:]
					params 			= splitData[4:]
					commandParams		= [command, user, host, channel, params ]
					self.commands.callCommand( commandParams )


if __name__ == "__main__":
	sjBot 		= sjBot()
