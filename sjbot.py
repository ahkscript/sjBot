#======================== sjBot v4+ ================================
# Author:		Steven J. Core ( Sjc1000 )
# Info:			IRC Bot
#===================================================================

#======================= imports ===================================
from multiprocessing import Process
import socket
import re
import json
import urllib2
import urllib
import random
import sys
import xml.etree.ElementTree as ElementTree
import HTMLParser
import time
import ast, operator
import ConfigParser
#====================================================================

#======================= Files ======================================
try:
	channelFile		= os.path.dirname(os.path.realpath(__file__)) + "/channels.txt"
	settingsIni		= os.path.dirname(os.path.realpath(__file__)) + "/conf.ini"
	dataFile 		= os.path.dirname(os.path.realpath(__file__)) + "/data"
except:
	channelFile 	= "channels.txt"
	settingsIni 	= "conf.ini"
	dataFile 	= "data"
#====================================================================


class sjBot(object):
	config 			= ConfigParser.ConfigParser()
	config.read(settingsIni)	
	password 		= config.get("details", "password")

	with open(channelFile) as file:
		channelList 	= file.readlines()

	file 			= open( dataFile )
	data 			= file.read()
	data 			= json.loads( data )
	chatObject 		= data["chat"]
	ontextObject		= data["commands"]
	weapons 		= data["weapons"]

	network     		= data["config"]["server"]
	port        		= data["config"]["port"]                 	
	botName        		= data["config"]["name"]
	botcmd 			= data["config"]["botcmd"]
	ownerlist 		= data["config"]["owners"]
	registeredName 		= data["config"]["registered"]

	paramData 		= ""
	output 			= ""
	owners 			= []
	owners.append("Sjc1000@unaffiliated/sjc1000")

	def __init__(self):
		self.irc 		= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.callCommand("joinserver")
		self.mainthread 	= Process(target=self.loop)
		self.mainthread.start()
	
	def callCommand(self, commandName, name="sys"):
		fileLocals 		= dict()
		if name != "sys":
			if self.ontextObject["commands"][name]["owner"] == 1 and not any( self.host == v  for v in self.owners):
				self.irc.send("PRIVMSG " + self.channel + " :You are not my master, " + self.user + "\r\n")
				return 1
		execfile("modules/" + commandName + ".py", {"self":self }, fileLocals )
		data 			= fileLocals["output"].replace("&botname", self.botName).replace("&botcmd", self.botcmd )
		if data != "__notext__":
			self.irc.send("PRIVMSG " + self.channel + " :" + data + "\r\n")
			


	def recieve(self, output=0, ammount=1024):
		data 		= self.irc.recv(ammount)
		if output:
			print( data )
		return data


	def loop(self):
		while 1:
			data 		= self.recieve(1)
			self.ircData 	= data

			file 			= open( dataFile )
			fdata 			= file.read()
			fdata 			= json.loads( fdata )
			self.chatObject 	= fdata["chat"]
			self.ontextObject	= fdata["commands"]
			self.weapons 		= fdata["weapons"]
			self.botcmd 		= fdata["config"]["botcmd"]
			#======================= On message stuff =============================
			for text in self.ontextObject["ontext"]:
				if text.replace("&botname", self.botName).replace("&server", self.ircData[6:] ) in data:
					thread 		= Process(target=self.callCommand, args=(self.ontextObject["ontext"][text],) )
					thread.start()
			#======================================================================


			dt 				= re.match(":(?P<User>.*?)!~?(?P<Host>.*?)\s(?P<Command>.*?)\s(?P<Channel>.*?)\s:(?P<Message>.*)\\r", data)

			if dt:
				self.user 		= dt.group("User")
				self.host 		= dt.group("Host")
				self.command 		= dt.group("Command")
				self.channel 		= dt.group("Channel")

				self.message 		= dt.group("Message")


				#====================== Chat stuff ====================================
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
								continue
							self.irc.send("PRIVMSG " + self.channel + " :" + response + "\r\n")
				#======================================================================


				#======================= Commands =============================
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
					
						for name in self.ontextObject["commands"]:
							for cmd in self.ontextObject["commands"][name]["cmd"]:
								if command == cmd:
									thread 		= Process(target=self.callCommand, args=(self.ontextObject["commands"][name]["file"],name,) )
									thread.start()
				#=================================================================

sjBot 		= sjBot()
