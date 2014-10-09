import irc
import imp
from os import listdir
import time
import sys
from queue import Queue
from threading import Thread
import os
import threading

class threads():
	def __init__(self, workers=4, queueSize=0):
		self.Queue 	= Queue(queueSize)

		for i in range(workers):
			thread 		= Thread(target=self.worker)
			thread.daemon 	= True
			thread.start()

		self.noWorkers 	= threading.active_count() - 1
	
	def worker(self):
		while True:
			task 		= self.Queue.get()
			try:
				function 	= getattr(task["module"], task["function"])
			except:
				continue


			if task["params"] == [""]:
				function()
			else:
				function(*task["params"])
			self.Queue.task_done()

	def call(self, commandName, params, module=__import__(__name__), join=0 ):
		if threading.active_count() -1 < self.noWorkers:
			self.addWorkers(1)

		if isinstance(params, str ):
			params 		= [ params ]
		self.Queue.put({"function": commandName, "module": module, "params": params} )
		if join:
			self.Queue.join()
		return 0

	def addWorkers(self, numOfWorkers ):
		for i in range( numOfWorkers ):
			thread 		= Thread(target=self.worker)
			thread.daemon 	= True
			thread.start()


'''
Class:		Plugin
Author:		Sjc1000
Description:	This is a class to easily load plugins into a python script.
Py Version:	It was built in Python3, i haven't tested it with 2.
Notes:		When specifying the PluginFolder you need to specify the trailing / otherwise it will not work.
Plugin File Example:

-------------------------------------------
metaData 	= {"key": "value"}

def execute(command, params ):
	* do stuff *
	return myValue
-------------------------------------------

'''
class plugin:
	''' __init__
			initiates all the variables.
			Then runs the loadPlugins to load the modules. ( Which also gets run each time you call .run()		
	'''	
	def __init__(self, pluginFolder ):
		self.pluginFolder	= pluginFolder
		self.commands 	= {}
		self.loadPlugins()
	
	''' loadPlugins
		Loads all the plugins into a variable which is classwide.
	'''
	def loadPlugins(self):	
		files 		= listdir(self.pluginFolder)
		self.commands 	= {}
		for x in files:
			if ".py" in x:
				current 		= imp.load_source(x[:-3]+"_plugin", self.pluginFolder + x )
				self.commands[x[:-3]] 	= current
		return 0	

	''' loadMeta
		Loads the metaData dictionary from the file. MetaName is the key in the metaData dict.
	'''
	def loadMeta(self, fromCommand, metaName ):
		metaData 		= self.commands[fromCommand].metaData
		if metaName in metaData:
			return metaData[metaName]
		else:
			return 0

	''' run
		Runs the command, this also supports the commandName being one of the aliases in the command.
		Returns the return value from the execute function of the module if it finds the right module, if not 0 is returned.
	'''
	def run(self, commandName, botCmd, irc, user, host, channel, params ):
		self.loadPlugins()
		for z in self.commands:
			if any( commandName == cmd for cmd in self.loadMeta(z, "aliases") ):
				if user[1] == 0 and self.commands[z].metaData["owner"] == 1:
					return "You are not an owner"
				else:
					return self.commands[z].execute((commandName, self.commands, botCmd, user[1], irc), user[0], host, channel, params)
		return 0

	def runE(self, commandName, *params ):
		return self.commands[commandName].execute(commandName, params )



class sjBot():

	# variables ================================
	botName 		= "sjBots"
	server			= "irc.freenode.net"
	port 			= 6667
	botCmd 			= ["."]
	ownerList 		= ["unafiliated/sjc1000"]
	channelList 		= ["#Sjc_Bot"]
	password 		= open(os.path.dirname(os.path.realpath(__file__)) + "/password", 'r').read()
	#===========================================

	def __init__(self):
		self.thread		= threads()
		self.irc 		= irc._irc(self.server, self.port)
		self.irc.joinserver(self.botName)
		self.processes 		= threads(8)
		self.plugins 		= plugin("plugins/")
		self.constant 		= plugin("constant/")
		self.main()


	def waitForChange(self, pluginName ):
		self.constant.commands[pluginName].execute(self.irc)
			

	# onPING
	#	When the bot recieves a ping message.
	def onPING(self, server ):
		self.irc.pong( server )
		return 0


	# on433
	#	When the bot tries to conenct and the username is already in use.
	def on433(self, host, ast, botName, *params ):
		self.irc.nick(botName + "_" )
		return 0

	# on376
	#	End of MOTD
	def on376(self, *params ):
		self.irc.login(self.password)
		time.sleep(5)
		self.irc.join(self.channelList )
		return 0

	# onJOIN
	#	When anyone joins a channel, including the bot.
	def onJOIN(self, host, channel ):
		user 		= host.split("!")[0][1:]
		if user == self.botName:
			time.sleep(5)
			self.irc.pMessage(channel, "Hello World!" )
			
			for cmd in self.constant.commands:
				self.processes.call("waitForChange", cmd, self)
		return 0


	# onPRIVMSG
	#	When the bot see's a PRIVMSG, this is any message, through the channel or PM.
	def onPRIVMSG(self, fullHost, channel, *message ):

		for btCmd in self.botCmd:
			if btCmd == message[0][1:len(btCmd)+1]:
				if self.botName in btCmd:
					command 	= message[1]
					params 		= message[2:]
				else:
					command 	= message[0][len(btCmd)+1:]
					params 		= message[1:]	
				user 		= fullHost.split("!")[0][1:]
				host 		= fullHost.split("!")[1]
				
				if channel == self.botName: 	# 
					channel = user		# 	These lines give sjBot the ability to respond in PM.

				sendData 	= self.callCommand(command,user,host,channel, params)
				if sendData:
					self.irc.pMessage(channel, sendData )

	
	# main
	#	The main loop.
	#	The bot recieves data from IRC then palms it off into the right section.
	def main(self):
		recData 	=  "something"
		while recData != "":		

			recData 	= self.irc.recv(1).split('\r\n')

			for split in recData:
				if split == '' or len( split.split(' ') ) < 2:
					continue

				splitData 	= split.split(' ')


				if splitData[0] == "PING":
					self.processes.call("onPING", splitData[1], self )
					continue

			
				command 	= splitData[1]
				splitData.remove(splitData[1] )			

				self.processes.call("on" + command, splitData, self )
				time.sleep(1)

	# isOwner
	#	Checks if a host is in the owner list.
	#	Returns 1 ( True ) if they are and 0 ( False ) if they aren't.
	def isOwner(self, host ):
		if any( str(host.split("@")[1]) == chost for chost in self.ownerList ):
			return 1
		else:
			return 0




	def callCommand(self, command, user, host, channel, rparams ):
		cmdNocaps 		= command		
		command 		= command.lower()
		commandList 		= []
		params 			= []

		for k in rparams:
			if k == "":
				continue

			params.append( k )

		
		self.plugins.loadPlugins()
		sendToChannel = self.plugins.run(command, self.botCmd, self.irc, [user, self.isOwner( host )], host, channel, params)
		if sendToChannel == 0:		
			sendToChannel = self.plugins.run("ahks",self.botCmd, self.irc, [user, self.isOwner( host )], host, channel, [command] + params)
		
		if isinstance( sendToChannel, str ):
			sendToChannel 		= sendToChannel.replace("&botcmd", self.botCmd[0] )
		else:
			for index,send in enumerate(sendToChannel):
				sendToChannel[index] 	= send.replace("&botcmd", self.botCmd[0] )

		if sendToChannel == "__notext__":
			return 0

		return sendToChannel




sjBot 		= sjBot()
