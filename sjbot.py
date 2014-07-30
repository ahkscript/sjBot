#============================================================================================================
#		Author: 		Steven J. Core ( Sjc1000 )
#		Program:		sjBot. irc bot.
#
#		Comments:		sjBot v5. v4 was a fun experiment while it lasted, but it
#					wasn't very practical. v5 will be super duper stable, i pinkie promise ;)
#============================================================================================================

#== Imports =================================================================================================
import socket
import re
import json
import sys
import time
import ConfigParser
import random
#============================================================================================================

try:
	settingsIni		= os.path.dirname(os.path.realpath(__file__)) + "/conf.ini"
	dataFile 		= os.path.dirname(os.path.realpath(__file__)) + "/data"
except:
	settingsIni 	= "conf.ini"
	dataFile 	= "data"


#== sjBot class =============================================================================================
class sjBot():
	sjbotsettings 	= open( settingsIni ).read()
	sjbotData 	= json.loads( open( dataFile ).read() )
	commands 	= sjbotData["commands"]
	server 		= sjbotData["data"]["server"]
	port 		= sjbotData["data"]["port"]
	botName 	= sjbotData["data"]["name"]
	botcmd 		= sjbotData["data"]["cmd"]
	channelList 	= sjbotData["data"]["channels"]
	chatObject 	= sjbotData["chat"]
	weapons 	= sjbotData["weapons"]
	owners		= sjbotData["data"]["owners"]
	config 		= ConfigParser.ConfigParser()
	config.read(settingsIni)	
	password 	= config.get("details", "password")
	
	
#============================================================================================================
	def __init__(self):
		self.irc 	= socket.socket(socket.AF_INET, socket.SOCK_STREAM )
		self.irc.connect((self.server, self.port))
		self.irc.send("NICK " + self.botName + " \r\n")
		self.irc.send("USER " + self.botName + " " + self.botName + " " + self.botName + " :Uptone Software\r\n")		


		self.run(1)
		
#============================================================================================================
	def callCommand(self, commandName, name="sys" ):
		fileOutput 	= dict()


		if name != "sys":
			if self.commands[name]["owner"] == 1 and not isOwner:
				self.irc.send("PRIVMSG " + self.channel + " :You are not my master, " + self.user + "\r\n")
				return 1

		execfile("modules/" + commandName + ".py", {"self": self}, fileOutput)

		odata 			= fileOutput["output"]	
		

		channel 	= odata["channel"]
		sendText 	= odata["text"]


		if channel == "__default__" and name != "sys":
			channel = self.channel

		sendText 	= sendText.replace("&botname", self.botName).replace("&botcmd", self.botcmd )
		if sendText != "__notext__":
			self.irc.send("PRIVMSG " + channel + " :" + sendText + "\r\n")
#============================================================================================================

	def onText(self, checkText):
		onText 		= self.sjbotData["on"]
		
		try:			
			for text in onText:
				if text.replace("&botname", self.botName).replace("&server", checkText[6:] ) in checkText:
					self.callCommand(onText[text])
		except UnicodeDecodeError:
			return 0
#============================================================================================================

	def onChat(self, checkText):
		try:				
			user 			= self.user
			message 		= self.message
			for x in self.chatObject:	
				for v in self.chatObject[x]["text"]:
					if ( v.replace("&botname", self.botName).lower() in message.lower() ):
						if any( b == user.lower()  for b in self.chatObject[x]["response"] ):
							response 		= random.choice( self.chatObject[x]["response"][user.lower()] ).replace("&user", user )				
						else:
							response 		= random.choice( self.chatObject[x]["response"]["__default__"] ).replace("&user", user )
						if ( response == "__notext__"):
							return 0
						self.irc.send("PRIVMSG " + self.channel + " :" + response + "\r\n")
		except UnicodeDecodeError:
			return 0

#============================================================================================================

	def isCommand(self, checkText ):
		commands 	= self.message.split('||')
		for cm in commands:
					

			self.params 	= cm.split(' ')

			index 		= 0

			for dex in self.params:
				if self.botcmd in dex:
					rIndex 	= index

				index 		= index + 1
						

			try:
				self.fullData 	= self.params[ rIndex + len(self.botcmd):]
				checkCmd 		= self.params[ rIndex ]
				command 		= self.params[ rIndex ]
				self.paramData 		= " ".join(self.params[rIndex + len(self.botcmd):])
			except:
				checkCmd 		= self.params[0]
				command 		= self.params[0]
				self.fullData 		= self.params[len(self.botcmd):]
				self.paramData 		= " ".join(self.params[len(self.botcmd):])


			if checkCmd[:len(self.botcmd)] == self.botcmd:
				command = command[len(self.botcmd):].lower()
					
				for name in self.commands:
					for cmd in self.commands[name]["cmd"]:
						if command == cmd:
							try:
								self.callCommand(self.commands[name]["file"], name)
							except:
								self.irc.send("PRIVMSG " + self.channel + " :Something went wrong!\r\n")

			time.sleep(1)


#============================================================================================================		
	def run(self, showlog=0):
		inText 		= "Something to start with"
	
		while inText:

			inText 		= self.irc.recv(1024)
			if showlog:
				print( inText )
			
			self.ircData 	= inText
			sjbotData 	= json.loads( open( dataFile ).read() )
			commands 	= sjbotData["commands"]
			server 		= sjbotData["data"]["server"]
			port 		= sjbotData["data"]["port"]
			botName 	= sjbotData["data"]["name"]
			botcmd 		= sjbotData["data"]["cmd"]
			channelList 	= sjbotData["data"]["channels"]
			chatObject 	= sjbotData["chat"]
			weapons 	= sjbotData["weapons"]
			owners		= sjbotData["data"]["owners"]

			self.onText(inText)	

			dt 				= re.match(":(?P<User>.*?)!~?(?P<Host>.*?)\s(?P<Command>.*?)\s(?P<Channel>.*?)\s:(?P<Message>.*)\\r", inText)

			if dt:
				self.user 		= dt.group("User")
				self.host 		= dt.group("Host")
				self.command 		= dt.group("Command")
				self.channel 		= dt.group("Channel")

				self.message 		= dt.group("Message")

				
				if self.channel == self.botName:
					self.channel = self.user

				
				try:
					self.onChat(inText)
					self.isCommand(inText)
				except UnicodeDecodeError:
					continue
				
				
			
		print("Closed connection. Restarting.")
		bot 			= sjBot()
#============================================================================================================


bot 		= sjBot()
