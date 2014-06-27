#################################################################################################################
#	Steven J. Core ( Sjc1000 )
#									
#	A simple IRC bot											
#################################################################################################################
#	This is just a simple IRC bot that was built for cool IRC things.					
#	It is really my first Python project. So it may not be the best or the nicest.				
#################################################################################################################



############################################# IMPORT ###########################################################
# 	Import all the needed extra's. Python doesn't include them by default. But still has them by default.
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
import thread
import ast, operator
import ConfigParser
import os
#################################################################################################################



############################################## USER VARIABLES ###################################################
#	Feel free to change all of these, they were put in variables like this so you can easily change them
# 	without having to change raw code.
network     	= 'irc.freenode.net'          	# The network to join to.	
port        	= 6667                         	# The port to join on ( 6667 is default ).

botName        	= "sjBot"                  	# The name to start with.
master      	= []
master.append( "Sjc1000@unaffiliated/sjc1000" )


try:
	channelFile		= os.path.dirname(os.path.realpath(__file__)) + "/channels.txt"
	settingsIni		= os.path.dirname(os.path.realpath(__file__)) + "/conf.ini"
except:
	channelFile 	= "channels.txt"
	settingsIni 	= "conf.ini"


version 		= "14"

with open(channelFile) as file:
	content 	= file.readlines()


config 			= ConfigParser.ConfigParser()
config.read(settingsIni)

password 		= config.get("details", "password")
ownerlist 		= config.items("owners")

loggedusers 	= []

for x in ownerlist:
	loggedusers.append({"user": x[0], "pass": x[1], "host": ""})
##################################################################################################################




##################################################################################################################
class commands():


	weapons 		= [
		"a small lion.",
		"a dictionary",
		"an angry mountain.",
		"the power of 3.",
		"a honey badger.",
		"a Hyper beam.",
		"a short drop and a sudden stop.",
		"a spoon, because knives are too easy.",
		"a bowtie.",
		"tlm.",
		"a rraaaiiinnboww trout.",
		"bordem."
	]

	apiKeys				= {
		"ahk": "009062493091172133168:_o2f4moc9ce",
		"wolfram": "9HX9YX-HJHHPWPVK4"
	}

	messageData  		= []

	colorCode 			= {
		"white" : "\x030",
		"black" : "\x031",
		"darkblue" : "\x032",
		"darkgreen" : "\x033",
		"red" : "\x034",
		"darkred" : "\x035",
		"darkviolet" : "\x036",
		"orange" : "\x037",
		"yellow" : "\x038",
		"lightgreen" : "\x039",
		"cyan" : "\x0310",
		"lightcyan" : "\x0311",
		"lightblue" : "\x0312",
		"pink" : "\x0313",
		"grey" : "\x0314",
		"silver" : "\x0315"
	}

	controlCode 		= {
		"bold" : "\x02",
		"italic" : "\x1D",
		"rcolor" : "\x0F",
		"reverse" : "\x16",
		"underline" : "\x1F"
	}



	def shortenUrl(self, url):
		mUrl 			= "http://tiny-url.info/api/v1/create?url=" +  url + "&provider=linkee_com&apikey=C77889685I98640AA4I&format=json"
		hdr 			= {'User-Agent': 'Mozilla/5.0'} 
		request 		= urllib2.Request( mUrl, headers=hdr)
		response 		= urllib2.urlopen( request)

		html			= response.read()
		output 			= json.loads( html)

		reData 			= output['shorturl']

		if reData:
			return reData
		else:
			return url


	def math(self, params):
		outputData 		= str( self.solve( self.fullData ) )
		return self.fullData + " = " + outputData


	def whoIs(self, params):
		return "My owner's host name is " + self.owner


	def google(self, params):
		return self.google_search(self.fullData)

	def google_search(self, query):
		search 			= urllib.quote( str(query))

		try:
			url				= 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=' + search 
			hdr 			= {'User-Agent': 'Mozilla/5.0'} 
			request 		= urllib2.Request( url, headers=hdr)
			response 		= urllib2.urlopen( request)

			html			= response.read()

			output 			= json.loads( html)
			title 			= output['responseData']['results'][0]['titleNoFormatting']
			url 			= output['responseData']['results'][0]['url']

			url 			= urllib.unquote( url).encode('utf-8')
			title 			= urllib.unquote( title).encode('utf-8')

			if len( url ) > 20:
				url 		= self.shortenUrl( url )

			return "\x02" + title + "\x02 - " + url
		except:
			return "\x02\x035No Data found\x02\x03"


	def weather(self, params):
	#http://api.openweathermap.org/data/2.5/weather?q=London,uk
		if len(params) < 0:
			return "Weather needs more params."

		try:
			url				= 'http://api.openweathermap.org/data/2.5/weather?q=' + self.paramData.replace(" ", "+") + "&units=metric"
			hdr 			= {'User-Agent': 'Mozilla/5.0'} 
			request 		= urllib2.Request( url, headers=hdr)
			response 		= urllib2.urlopen( request)
			html			= response.read()
			output 			= json.loads( html)


			weather 		= output["weather"][0]["description"]
		

			windspeed 		= str( output["wind"]["speed"] ) + " km/h"

			try:
				windgust 		= "a gust of " +str( output["wind"]["gust"] ) + " km/h"
			except:
				windgust 		= "no gust"

			winddirection 	= output["wind"]["deg"]
			city 			= output["name"]

			if winddirection > 45 and winddirection < 135:
				winddirection	= "westerly" 
			if winddirection > 135 and winddirection < 225:
				winddirection 	= "northerly"
			if winddirection > 225 and winddirection < 315:
				winddirection	= "easterly"
			if winddirection > 315 and winddirection < 45:
				winddirection 	= "southerly"

			if city 		== "":
				city 		= output["sys"]["country"]

			temperature 	= output["main"]["temp"]
			humidity		= str( output["main"]["humidity"] ) + "%"

			return "The weather in " + city + " : " + weather + ", with a temperature of " + str( temperature ) + " c ( " + str( temperature*9/5+32  ) + " F ) and a humidity of " + humidity  + ". The wind is a " + winddirection + " at " + windspeed + " with " +  windgust
		except:
			return "Could not find the weather for " + self.paramData

	def rss(self, params):

		try:
			number 			= int( params[0] )
		except IndexError:
			number 			= 5
		except ValueError:
			return "Please use a number for this paramater."

		if len( params ) > 1:
			self.channel 	= params[1]

		if number > 10:
			number 		= 10

		url				= 'http://ahkscript.org/boards/feed.php'
		hdr 			= {'User-Agent': 'Mozilla/5.0'} 
		request 		= urllib2.Request( url, headers=hdr)
		response 		= urllib2.urlopen( request)
		xml				= response.read()
		xml 			= unicode(xml, errors='ignore')

		xmlmatch 		= re.findall("<entry>.*?<author><name><.*?\[.*?\[(.*?)\]\]>.*?<updated>(.*?)<.*?<published>(.*?)</published>.*?<id>(.*?)</id>.*?<title.*?><.*?\[.*?\[(.*?)\]\]></title>", xml, re.S)
		
		i 				= 0

		output 			= ""

		while i < number:
			name 			= xmlmatch[i][0]
			updated 		= xmlmatch[i][1]
			published 		= xmlmatch[i][2]
			link 			= HTMLParser.HTMLParser().unescape(xmlmatch[i][3])
			title 			= HTMLParser.HTMLParser().unescape(xmlmatch[i][4])

			self.Message(self.channel, "" + title + " - " + name + " : " + link )
			i                       = i + 1

		return "found the last " + str( number ) + " posts."


	def hello(self, params):
		if len(params) > 0:
			user 		= params[0]
		else:
			user 		= self.user
		return "Hey there " +  user + " :D"

	def join(self, params):

		for k in params[0:]:
			self.Join(k)

		return "notext"

	def leave(self, params):

		for k in params[0:]:
			self.Part(k)

		return "notext"


	def aRss(self, params):

		if len(params) > 0:
			self.autorss 		= params[0]
		else:
			self.autorss 		= 1

		if self.autorss == 1:
			return "Now automatically grabbing rss data."
		else:
			return "Not grabbing rss data."

	def channels(self, params):
		output 			= "I am currently in the channels, "
		
		for k in self.channelList:
			output 		= output + k + " "

		return output


	def ahk(self, params):
		return self.google_search("autohotkey: " + str( self.paramData) )


	def help(self, params):
		
		try:
			if len( params ) > 0:
				return self.cmdInfo[params[0]]
		except:
			return "That did not match any of my commands."

		
		output 		= ""
		for com in self.cmdInfo:
			output 	= output  + com + " | "

		return output + " Use !help [command name] to get more info."

	def whoIsOnline(self, params): #are <strong>(.*?)</strong> users     <--regex
		url			= 'http://ahkscript.org/boards/'
		hdr 			= {'User-Agent': 'Mozilla/5.0'} 
		request 		= urllib2.Request( url, headers=hdr)
		response 		= urllib2.urlopen( request)
		html			= response.read()
		print( html )
		reg 			= re.match(".*?<strong>(?P<users>\d+)</strong> users.*?", html, re.S )
		return str( reg.group("users") ) + " users currently online at the forum."


	def newestMem(self, params):
		return "This command is still a work in progress."


	def totalPosts(self, params):
		return "This command is still a work in progress."


	def totalTopics(self, params):
		return "This command is still a work in progress."

	def totalMems(self, params):
		return "This command is still a work in progress."

	def stop(self, params):
		sys.exit()


	def kill(self, params):
		weapon 		= ""


		if len( params ) > 1:
			for k in params[1:]:
				weapon 	= weapon + k + " "
		else:
			weapon 		= random.choice( self.weapons )
			

		if len(params ) > 0:
			killWho 	= params[0]
		else:
			return "I require more params for this command."


		return "\x01ACTION Kills " + killWho + " with " + weapon + "\x01"


	def dance(self, params):
		c 		= self.colorCode
		return c["orange"] + "Danceroo! :D " + c["cyan"] + "yay " + c["red"] + "yay " + c["lightgreen"] + "yay! " + c["darkblue"] + "\(^_^)/ :D\x03"

	def paste(self, params):
		if len(params ) > 0:
			return params[0] + ", Please paste your code at http://www.bpaste.net"
		return "Please paste your code at http://www.bpaste.net"

	def login(self, params):
		if len( params ) < 1:
			return "Not enough params passed to login, Please specify both username and password."

		if any( c["user"].lower() == params[0].lower()  for c in loggedusers ):
			i = 0		
			while( i < len( loggedusers ) ):
				if ( loggedusers[i]["user"].lower() == params[0].lower() ):
					break
				i 	= i + 1

			if ( loggedusers[i]["user"].lower() == params[0].lower() and loggedusers[i]["pass"] == params[1] ):
				loggedusers[i]["host"]   = self.host
				if ( any( c == self.host  for c in master )):
					return "Already logged in!"
				
				master.append( self.host )
				return "Logged in!"
	

		return "Could not login"

	def changePass(self, params):
		if len( params ) < 0:
			return "Not enough params passed to change password, please specify a password to change to."
		i = 0
	
		if any( c["host"].lower() == self.host.lower()  for c in loggedusers ):
			while( i < len( loggedusers ) ):
				if ( loggedusers[i]["host"].lower() == self.host.lower() ):
					break
				i 	= i + 1
			print( loggedusers[i]["user"] + " " +  params[0] )
			config.set("owners", loggedusers[i]["user"], params[0] )
			with open(settingsIni, 'wb') as configfile:
				config.write( configfile )

			return "Password has been changed!"

		return "Could not change password"

##################################################################################################################


##################################################################################################################
class sjBot(commands):

	bot_cmd 		= "!"
	commandList 	= {
		"hello" : commands.hello,
		"hey" : commands.hello,
		"hi" : commands.hello,
		"g" : commands.google,
		"google" : commands.google,
		"rss" : commands.rss,
		"feed" : commands.rss,
		"we" : commands.weather,
		"weather" : commands.weather,
		"join" : commands.join,
		"leave" : commands.leave,
		"autorss" : commands.aRss,
		"channels" : commands.channels,
		"ahk" : commands.ahk,
		"a" : commands.ahk,
		"help" : commands.help,
		"commands" : commands.help,
		"stop" : commands.stop,
		"owner" : commands.whoIs,
		"kill" : commands.kill,
		"k" : commands.kill,
		"dance" : commands.dance,
		"d" : commands.dance,
		"p" : commands.paste,
		"paste" : commands.paste,
		"online" : commands.whoIsOnline,
		"login" : commands.login,
		"changepass" : commands.changePass,
		"cp" : commands.changePass
	}
	cmdInfo 			= {
		"hello" : "This command will say hello to the user, or optionally say hello to someone in specific. !hello [user]",
		"hey" : "This command will say hello to the user, or optionally say hello to someone in specific. !hey [user]",
		"hi" : "This command will say hello to the user, or optionally say hello to someone in specific. !hi [user]	",
		"google" : "This command will search google with a specified query. !google <query>",
		"rss" : "This command will show the latest posts on ahkscript. With an optional specified ammount. !rss [ammount]",
		"weather" : "This command will show weather for a specified location. !weather <location>",
		"join" : "This command will join a channel, only usable by the bots master. !join <channel1> [channel2] etc.",
		"stop" : "Stops the process. Only the bots mater can use this. !stop",
		"ahk" : "Searches the forum for something. !ahk <query>",
		"help" : "Gives info about commands. !help <command>",
		"stop" : "Stops the bot, only usable by the bots master. !stop",
		"owner" : "Makes the bot say who the master is. !owner",
		"kill" : "Kills a specified user with either a random or specified weapon. !kill <user> [weapon]",
		"dance" : "Makes the bot dance :D. !dance",
		"paste" : "Tells a user to paste their code at bpaste.net. !paste [user]",
		"online" : "Shows how many users are online at the forum. !online"
	}
	ownerCommands	= [
		"join", "leave", 'autoRss', "stop"
	]
	owner 			= "Sjc1000@unaffiliated/sjc1000"
	autorss 		= 0
	channelList 	= []
	trusted_channels 	= [
		"#ahk",
		"#ahkscript",
		"#Sjc_Bot"
	]


	def __init__(self, network, port, nickname, user, password):
		self.irc 		= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.irc.connect((network, port))
		self.irc.send("NICK " + nickname + " \r\n")
		self.irc.send("USER " + user + " " + user + " " + user + " :Uptone Software\r\n")
		self.irc.send("PRIVMSG NickServ :Identify " + nickname + " " + password + "\r\n")

	def Message(self, toWho, text):
		self.irc.send( "PRIVMSG " + toWho  + " :" +text + "\r\n")

	def Notice(self, toWho, text):
		self.irc.send("NOTICE " + toWho + " :" + text + "\r\n")

	def Join(self, channel):
		self.channelList.append(channel)
		self.irc.send("JOIN " + channel + "\r\n")

	def Part(self, channel):
		self.channelList.remove(channel)
		self.irc.send("PART " + channel + "\r\n")

	def Pong(self, server): #PING :verne.freenode.net  - EXAMPLE	
		self.irc.send("PONG :" + server + "\r\n")

	def callCommand(self, commandName):

		if any( c == commandName  for c in self.ownerCommands ) and any( c != self.owner  for c in master ):
			return "You are not my master. " + self.user + "."
		else:
			return self.commandList[ commandName](self, self.fullData)


	def Start(self):
		#self.thread 		= Timer(30, self.autoRss)
		#self.thread.start()
		return self.loop()


	#def autoRss(self):

	#	while 1:
	#		self.thread.start()

#			if self.autorss == 0:
#				continue
#
#
#			if 'last' not in locals():
#				last 		= ""
#
#			url				= 'http://ahkscript.org/boards/feed.php'
#			hdr 			= {'User-Agent': 'Mozilla/5.0'} 
#			request 		= urllib2.Request( url, headers=hdr)
#			response 		= urllib2.urlopen( request)
#			xml				= response.read()
#			xml 			= unicode(xml, errors='ignore')
#
#
#			if last == xml:
#				continue
#
#			last 			= xml
#
#			xmlmatch 		= re.findall("<entry>.*?<author><name><.*?\[.*?\[(.*?)\]\]>.*?<updated>(.*?)<.*?<published>(.*?)</published>.*?<id>(.*?)</id>.*?<title.*?><.*?\[.*?\[(.*?)\]\]></title>", xml, re.S)
#			name 			= xmlmatch[0][0]
#			updated 		= xmlmatch[0][1]
#			published 		= xmlmatch[0][2]
#			link 			= HTMLParser.HTMLParser().unescape(xmlmatch[0][3])
#			title 			= HTMLParser.HTMLParser().unescape(xmlmatch[0][4])
#
#
#
#			for ch in self.channelList:
#				self.Message(ch, name + " - " + title + " : " + link )




	def loop(self):
		data 			= 1

		while data:
			
			try:
				data 		= self.irc.recv(1024)
				print( data )
			except:
				time.sleep(60)
				thread.start_new_thread(self.loop, ())

			dt 				= re.match(":(?P<User>.*?)!~?(?P<Host>.*?)\s(?P<Command>.*?)\s(?P<Channel>.*?)\s:(?P<Message>.*)\\r", data)

			if data[0:4] == "PING":
				self.irc.send("PONG :" + data[6:] + " \r\n")

			if dt:
				self.user 		= dt.group("User")
				self.host 		= dt.group("Host")
				self.command 	= dt.group("Command")
				self.channel 	= dt.group("Channel")

				self.message 	= dt.group("Message")

				
				commands 	= self.message.split('||')
				for cm in commands:
					

					self.params 	= cm.split(' ')

					index 		= 0

					for dex in self.params:
						if self.bot_cmd in dex:
							rIndex 	= index

						index 		= index + 1
						

					try:
						self.fullData 	= self.params[ rIndex + 1:]
						checkCmd 		= self.params[ rIndex ]
						command 		= self.params[ rIndex ]
						self.paramData 		= " ".join(self.params[rIndex + 1:])
					except:
						checkCmd 		= self.params[0]
						command 		= self.params[0]
						self.fullData 		= self.params[1:]
						self.paramData 		= " ".join(self.params[1:])


					if checkCmd[:1] == self.bot_cmd:
						command = command[1:].lower()


						if any( command == c  for c in self.commandList):
							output 			= self.callCommand( command )
							
							if output != "notext":
								if self.channel == botName:
									self.channel = self.user
								
								self.Message(self.channel, output )

##################################################################################################################



sjBot 		= sjBot(network, port, botName, botName, password)

for chan in content:
	sjBot.Join(chan)


sjBot.Start()
