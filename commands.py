import random
import urllib.request
import json
import sys

class _commands():
	

	def __init__(self, irc, botCmd):
		print("Commands module imported.")
		self.botCmd 	= botCmd
		self.irc 	= irc
		self.user 	= ""
		self.host 	= ""
		self.channel 	= ""	
		self.more 	= []
		self.ownerList 	= ["~Sjc1000"]


	def urlDownload(self, url ):
		try:
			response 	= urllib.request.urlopen(url) 
		except UnicodeEncodeError:
			return "Aww maaaaaan. I ran into some jank characters there. Decode error, sorry :P"
		except:
			return "__notext__"

		return response.read().decode('utf-8')


	def isOwner(self, user ):
		try:
			whoisData 	= str( self.irc.whoIs( user ) ).split(' ')
			if any( whoisData[4] == owner  for owner in self.ownerList ):
				return 1
			else:
				return 0
		except IndexError:
			return 0


	def callCommand(self, params ):
		command 		= params[0]
		self.user		= params[1]
		self.host 		= params[2]
		self.channel		= params[3]
		
		self.commandList 	= []
		params 			= params[4]
		index 			= 0

		for k in params:
			if k == "":
				params.remove(k)
				continue

			params[index] 	= k
			index 		= index + 1
		

		isOwner 		= self.isOwner(self.user)


		for cmd in commands:
			for ali in commands[cmd]['ali']:
				self.commandList.append( ali )

		
		if all( cmd != command  for cmd in self.commandList ):
			params 		= [command] + params
			self.irc.pMessage( self.channel, commands["ahk"]["run"](self, params) )
			return 0

		for cm in commands:
			for ali in commands[cm]["ali"]:
				if ali == command:
			
					if isOwner == 0 and commands[cm]["owner"] == 1:
						self.irc.pMessage( self.channel, ["You are not a registered owner.", "If you are, try logging into freenode then using the command again."] )			
						return 0
					sendToChannel 		= commands[cm]["run"](self, params )
					if sendToChannel == "__notext__":
						return 0
					self.irc.pMessage( self.channel, sendToChannel )
		return 0


	def hi(self, params):

		if params:
			self.user 	= params[0] 
		else:
			self.user 	= self.user

		responses 	= ["Hi there " + self.user, "Hey " + self.user + " :D", "Hiii " + self.user, "Hawwt daamn, Hi " + self.user + " :)"]		
		return random.choice( responses )

	
	def join(self, params ):
		self.irc.join( params )
		return "__notext__"

	
	def leave(self, params ):
		self.irc.leave( params )
		return "__notext__"


	def ahksearch(self, params): #http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=query&009062493091172133168:_o2f4moc9ce
		try:		
			self.more 	= []
	
			if len( params ) == 0:
				return "This command needs more params"
		
			search 		= '%20'.join( params ).replace("\r\n", "")
		
			htmlData 	= self.urlDownload( "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=" + search + "&cx=009062493091172133168:_o2f4moc9ce" )		
			if htmlData == "__notext__":
				return ["No data found!"]

			response	= json.loads( htmlData )
			title 		= response["responseData"]["results"][0]["titleNoFormatting"]
			url 		= response["responseData"]["results"][0]["url"]

			for more in response["responseData"]["results"][1:]:
				self.more.append( urllib.parse.unquote( more["titleNoFormatting"] ) + " - " + more["url"] )
		except IndexError:
			return ["No data found!"]
		return urllib.parse.unquote( title ) + " - " + url


	def help(self, params):

		if params:
			if all( cmd != params[0]  for cmd in self.commandList ):
				return ["The command " + params[0] + " is not recognised."]
			
			for cmd in commands:
				if any( params[0] == cm  for cm in commands[cmd]["ali"] ):
					commandName 		= cmd
			return [ "[ ] are optional params and < > are needed", commands[commandName]['help'].replace("&botcmd", self.botCmd) ]
		

		commandList 		= "Here is a list of commands"
		
		for cm in commands:
			commandList 	= commandList + " | " + cm

		return ["Use " + self.botCmd + "help [command name] for more info.", commandList]



	def google(self, params):
		self.more 	= []

		if len( params ) == 0:
			return "This command needs more params"
		
		search 		= '%20'.join( params )
		
		htmlData 	= self.urlDownload( "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=" + search )	

		if htmlData == "__notext__":
			return ["No data found!"]
	
		response	= json.loads( htmlData )


		title 		= response["responseData"]["results"][0]["titleNoFormatting"]
		url 		= response["responseData"]["results"][0]["url"]
		
		for more in response["responseData"]["results"][1:]:
			self.more.append( urllib.parse.unquote( more["titleNoFormatting"] ) + " - " + more["url"] )

		return urllib.parse.unquote( title ) + " - " + url



	def weather(self, params ):
		#http://api.openweathermap.org/data/2.5/weather?q=London,UK

		if len( params ) == 0:
			return "This command needs more params"

		search 		= '%20'.join( params )
		htmlData 	= self.urlDownload("http://api.openweathermap.org/data/2.5/weather?units=metric&q=" + search )

		if htmlData == "__notext__":
			return ["No data found!"]

		response 	= json.loads( htmlData )

		try:
			returnData 	= "The weather in " + response['name'] + " is "
		except KeyError:
			return ["Could not find the weather for " + search ]

		for we in response["weather"]:
			returnData 	= returnData + we["description"] + ", "

		returnData 	= returnData + "with a temperature of " + str( response["main"]["temp"] ) + "°C and a humidity of " + str( response["main"]["humidity"] ) + "."

		return [returnData]


	def more(self, params ):
		
		if len( self.more ) == 0:
			return ["No more data."]
		if len( params ) == 0:
			count 		= 1
		else:
			count 		= params[0]		

		moreData 		= ["More Data:"]
		index 			= 0
		while( int( index ) < int( count ) ):
			if len( self.more ) == 0:
				moreData.append("No more data.")
				break

			moreData.append( self.more[index] )
			self.more.remove( self.more[index] )

		return moreData
	

	def kill(self, params ):
		weapons 		= [	"a small lion.",
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



		if len( params ) == 0:
			return ["Please specify a person to kill.", commands["kill"]["help"].replace("&botcmd", self.botCmd ) ]

		if len( params ) < 2:
			weapon 		= random.choice( weapons )
		else:
			weapon 		= ' '.join( params[1:] )

		user 		= params[0]


		return "\x01ACTION Kills " + str( user ) + " with " + weapon + "\x01"


	def dance(self, params ):
		dance  	= ["DANCE! <(^_^)> >(^_^)> <(^_^)< ^(^_^)^ v(^_^)v", "WOOO yea, dance time! <(^_^)> >(^_^)> <(^_^)< ^(^_^)^ v(^_^)v", "I don't feel like dancing.... LOL JKS! <(^_^)> >(^_^)> <(^_^)< ^(^_^)^ v(^_^)v"]
		colorCode 	= [ "\x032", "\x033","\x034", "\x035", "\x036", "\x037","\x038", "\x039","\x0310","\x0311","\x0312","\x0313","\x0315" ]

		returnData 	= ""
		
		danceChoice 	= random.choice( dance ).split(' ')
		for x in danceChoice:
			returnData 	= returnData + random.choice(colorCode ) + x + "\x03" + " "

		return returnData 

	

	def imdb(self, params ):
		if len( params ) == 0:
			return [ "Please specify a movie to search for.", commands["imdb"]["help"].replace("&botcmd", self.botCmd ) ]


		search 		= '%20'.join( params )
		htmlData 	= self.urlDownload("http://www.omdbapi.com/?t=" + search )
		responseData 	= json.loads( htmlData )
		print( responseData )

		try:
			title 		= responseData["Title"]
			year 		= responseData["Year"]
			url 		= "http://www.imdb.com/title/" + responseData["imdbID"]
			plot 		= responseData["Plot"]
		except KeyError:
			return ["Could not find the movie info for " + ' '.join( params )]

		return [ title + " (" + year + ") - " + plot, url ]


	def ud(self, params ):
		if len( params ) == 0:
			return ["Please specify a word to search the Urban Dictionary for.", commands["ud"]["help"].replace("&botcmd", self.botCmd ) ]

		search 		= '%20'.join( params )
		url 		= "http://urbanscraper.herokuapp.com/define/" + search
		htmlData 	= self.urlDownload( url )
		try:
			jsonData 	= json.loads( htmlData )
		except ValueError:
			return ["Could not find an entry for " + ' '.join( params ) ]

		term 		= str( jsonData["term"] )
		definition 	= str( jsonData["definition"] ).split('\r')
		odef 		= []
		for x in definition:
			odef.append( x.replace('\\',"") )		
		
		returnData	= [term + " :"] + odef

		return 	returnData


	def stop(self, params ):
		sys.exit(0)
		

commands 		= { 

	"hi": {"ali": ["hi", "hello", "howdy", "hey"], "run": _commands.hi, "owner": 0, "help": "This command will say hi to the user. &botcmdHi [user]" },
	"ahk": {"ali": ["a", "ahk"], "run": _commands.ahksearch, "owner": 0, "help": "This command will search ahk for a query &botcmdahk <query>" },
	"help": {"ali": ["h", "help", "commands"], "run": _commands.help, "owner": 0, "help": "This command will show a list of commands. &botcmdhelp [command name]" },
	"google": {"ali": ["g", "google", "search"], "run": _commands.google, "owner": 0, "help": "This command will google for a query. &botcmdgoogle <query>" },
	"weather": {"ali": ["w", "weather"], "run": _commands.weather, "owner": 0, "help": "This command will find weather for a specific area. &botcmdweather <place>" },
	"more": {"ali": ["m", "more", "gimme_more"], "run": _commands.more, "owner": 0, "help": "This command will show more data from the last search. &botcmdmore [ammount]" },
	"kill": {"ali": ["k", "kill"], "run": _commands.kill, "owner": 0, "help": "This command will kill a user with a random or specified weapon. &botcmdkill <who> [weapon]" },
	"stop": {"ali": ["stop", "quit"], "run": _commands.stop, "owner": 1, "help": "This command will stop the execution of the bot. &botcmdstop" },
	"join": {"ali": ["join", "j"], "run": _commands.join, "owner": 1, "help": "This command will make the bot join channel/s. &botcmdjoin <channel 1> [channel 2] [channel 3] etc. " },
	"leave": {"ali": ["leave", "l"], "run": _commands.leave, "owner": 1, "help": "This command will make the bot leave channel/s. &botcmdleave <channel 1> [channel 2] [channel 3] etc." },
	"dance": {"ali": ["dance", "d", "move_yo_booty"], "run": _commands.dance, "owner": 0, "help": "This command will make the bot dance, &botcmddance"},
	"imdb": {"ali": ["movie", "imdb"], "run": _commands.imdb, "owner": 0, "help": "This command will search for a movie. &botcmdimdb <movie name>" },
	"ud": {"ali": ["dict", "define", "ud"], "run": _commands.ud, "owner": 0, "help": "This command will define a term. &botcmdud <term>" }
}
