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

botName        	= "sjBot"                  	# The name to start with.                    	# The command, so the bot knows its being told to do something.
master      	= "Sjc1000@unaffiliated/sjc1000"    	# The master of the bot ( the one who can use the master commands ).


try:
	channelFile		= os.path.dirname(os.path.realpath(__file__)) + "/channels.txt"
	settingsIni		= os.path.dirname(os.path.realpath(__file__)) + "/conf.ini"
except:
	channelFile 	= "channels.txt"
	settingsIni 	= "conf.ini"


version 		= "3.0.01.02"

with open(channelFile) as file:
	content 	= file.readlines()


config 			= ConfigParser.ConfigParser()
config.read(settingsIni)

password 		= config.get("details", "password")
##################################################################################################################




############################################ IRC VARS ############################################################
## see https://github.com/myano/jenni/wiki/IRC-String-Formatting
class ColorCode:
	White 		= '00'	# < White
	Black 		= '01'	# < Black
	DarkBlue 	= '02'	# < Dark blue
	DarkGreen 	= '03'	# < Dark green
	Red 		= '04'	# < Red
	DarkRed 	= '05'	# < Dark red
	DarkViolet 	= '06'	# < Dark violet
	Orange 		= '07'	# < Orange
	Yellow 		= '08'	# < Yellow
	LightGreen 	= '09'	# < Light green
	Cyan 		= '10'	# < Cornflower blue
	LightCyan 	= '11'	# < Light blue
	Blue 		= '12'	# < Blue
	Violet 		= '13'	# < Violet
	DarkGray 	= '14'	# < Dark gray
	LightGray 	= '15'	# < Light gray

class ControlCode:
	Bold		= '\x02'	# < Bold
	Color		= '\x03'	# < Color
	Reverse		= '\x16'	# < Reverse
	Reset		= '\x0F'	# < Reset
	Italic		= '\x09'	# < Italic
	Italic2		= '\x1D'	# < Italic
	Strike		= '\x13'	# < Strike-Through
	Underline	= '\x15'	# < Underline
	Underline2	= '\x1F'	# < Underline
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


	def google(self, params):
		return google_search(self.fullData)

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
			if winddirection > 315 and winddirection < 360:
				winddirection 	= "southerly"

			if city 		== "":
				city 		= output["sys"]["country"]

			temperature 	= output["main"]["temp"]
			humidity		= str( output["main"]["humidity"] ) + "%"

			return "The weather in " + city + " : " + weather + ", with a temperature of " + str( temperature ) + " c ( " + str( temperature*9/5+32  ) + " F ) and a humidity of " + humidity  + ". The wind is a " + winddirection + " at " + windspeed + " with " +  windgust
		except:
			return "Could not find the weather for " + self.paramData

	def rss(self, params):

		if len( params ) < 0:
			number 		= 5
		else:
			if params[0].isdigit():
				number	= int( params[0] )
			else:
				number = 5

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

	def dance(self, params):
		c = ControlCode.Color
		cOrange	= c + ColorCode.Orange
		cViolet	= c + ColorCode.Violet
		cRed	= c + ColorCode.Red
		cGreen	= c + ColorCode.LightGreen
		cCyan	= c + ColorCode.LightCyan
		cBlue	= c + ColorCode.Blue
		return cOrange + "Danceroo! :D " + cViolet + "yay " + cRed + "yay " + cGreen + "yay! " + cCyan + "\\(^_^)/ " + cBlue + ":D"

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

	def WhoIsOnline(self, params):
		return "This command is still a work in progress."


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

##################################################################################################################


##################################################################################################################
class sjBot(commands):

	def __init__(self, network, port, nickname, user, password):
		self.irc 		= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.irc.connect((network, port))
		self.irc.send("NICK " + nickname + " \r\n")
		self.irc.send("USER " + user + " " + user + " " + user + " :Uptone Software\r\n")
		self.irc.send("PRIVMSG NickServ :Identify " + nickname + " " + password + "\r\n")


		################### Variables         ###################
		self.bot_cmd 		= "!"
		self.commandList 	= {
				"hello" : commands.hello,
				"hey" : commands.hello,
				"hi" : commands.hello,
				"dance" : commands.dance,
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
				"stop" : commands.stop
		}
		self.cmdInfo 			= {
				"hello" : "This command will say hello to the user, or optionally say hello to someone in specific. !hello [user]",
				"hey" : "This command will say hello to the user, or optionally say hello to someone in specific. !hey [user]",
				"hi" : "This command will say hello to the user, or optionally say hello to someone in specific. !hi [user]	",
				"google" : "This command will search google with a specified query. !google <query>",
				"rss" : "This command will show the latest posts on ahkscript. With an optional specified ammount. !rss [ammount]",
				"weather" : "This command will show weather for a specified location. !weather <location>",
				"join" : "This command will join a channel, only usable by the bots master. !join <channel1> [channel2] etc.",
				"stop" : "Stops the process. Only the bots mater can use this. !stop",
				"ahk" : "Searches the forum for something. !ahk <query>"
		}
		self.ownerCommands	= [
			"join", "leave", 'autoRss', "stop"
		]
		self.owner 			= "Sjc1000@unaffiliated/sjc1000"
		self.autorss 		= 0
		self.channelList 	= []
		self.trusted_channels 	= [
			"#ahk",
			"#ahkscript",
			"#Sjc_Bot"
		]
		#########################################################

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

		if any( c == commandName  for c in self.ownerCommands ) and self.host != self.owner:
			return "You are not my master. " + self.user + "."
		else:
			return self.commandList[ commandName](self, self.fullData)


	def Start(self):
		#thread.start_new_thread(self.autoRss, ())
		return self.loop()


	#def autoRss(self):

	#	while 1:
	#		time.sleep(60)

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
						self.paramData 			= " ".join(self.params[1:])
					except:
						checkCmd 		= self.params[0]
						command 		= self.params[0]
						self.fullData 	= self.params[1:]
						self.paramData 			= " ".join(self.params[1:])


					if checkCmd[:1] == self.bot_cmd:
						command = command[1:].lower()


						if any( command == c  for c in self.commandList):
							output 			= self.callCommand( command )

							if output != "notext":
								self.Message(self.channel, output )

##################################################################################################################



sjBot 		= sjBot(network, port, botName, botName, password)

for chan in content:
	sjBot.Join(chan)


sjBot.Start()
