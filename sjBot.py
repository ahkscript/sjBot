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
import ast, operator
import ConfigParser
#################################################################################################################


############################################## USER VARIABLES ###################################################
#	Feel free to change all of these, they were put in variables like this so you can easily change them
# 	without having to change raw code.
network     	= 'irc.freenode.net'          	# The network to join to.	
port        	= 6667                         	# The port to join on ( 6667 is default ).

botName        	= "sjBot"                  	# The name to start with.
bot_cmd     	= "!"                        	# The command, so the bot knows its being told to do something.
master      	= "Sjc1000@unaffiliated/sjc1000"    	# The master of the bot ( the one who can use the master commands ).

commandLength	= len( bot_cmd)					# Gets the length of the bot command.

channelFile		= "channels.txt"
settingsIni		= "conf.ini"

version 		= "2.0"

with open(channelFile) as file:
	content 	= file.readlines()

config 			= ConfigParser.ConfigParser()
config.read(settingsIni)

password 		= config.get("details", "password")
##################################################################################################################


############################################ PROGRAM VARIABLES ###################################################
weapons 		= [
	"a small lion.",
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

trusted_channels 	= [
	"#ahk",
	"#ahkscript",
	"#Sjc_Bot",
	"#twdev.net"
]

apiKeys				= {
	"ahk": "009062493091172133168:_o2f4moc9ce",
	"wolfram": "9HX9YX-HJHHPWPVK4"
}

docList				= 'https://raw.githubusercontent.com/nimdahk/AHKLink/master/AHKLink_index.tsv'
try:
	url				= 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=' + search 
	hdr 			= {'User-Agent': 'Mozilla/5.0'} 
	request 		= urllib2.Request( url, headers=hdr)
	response 		= urllib2.urlopen( request)

	docList			= response.read()
except:
	docList 		= "Did not cache doc data."


messageData 		= []
##################################################################################################################


##################################################################################################################
binOps = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.div,
    ast.Mod: operator.mod
}

def solve(s):
    node = ast.parse(s, mode='eval')

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.Str):
            return node.s
        elif isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            return binOps[type(node.op)](_eval(node.left), _eval(node.right))
        else:
            raise Exception('Unsupported type {}'.format(node))

    return _eval(node.body)


def google_search( query ):
	search 			= urllib.quote(query)

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
			url 		= shortenUrl( url )

		return "\x02" + title + "\x02 - " + url
	except:
		return "\x02\x035No Data found\x02\x03"


# 	http://tiny-url.info/api/v1/create?url=https://www.google.com&provider=clicky_me&apikey=C77889685I98640AA4I
def shortenUrl( url ):
	mUrl 			= "http://tiny-url.info/api/v1/create?url=" +  url + "&provider=clicky_me&apikey=C77889685I98640AA4I&format=json"
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

def google():
	data 		= google_search(paramData)

	if data == "":
		irc.send("PRIVMSG " + channel + " :NO DATA FOUND\r\n")
	else:
		irc.send("PRIVMSG " + channel + " :" + data + "\r\n")




def math():
	try:
		outputData 		= str( solve( paramData ) )
		print( outputData )

		irc.send("PRIVMSG " + channel + " :\x02" + paramData + "\x02 - " + outputData + "\r\n")
	except:
		irc.send("PRIVMSG " + channel + " :Sorry, i cannot solve that.\r\n")


def kill():
	killWho 			= paramData
	killWith 			= random.choice( weapons )

	irc.send("PRIVMSG " + channel + " :\x01ACTION Kills " + killWho + " with " + killWith + "\x01\r\n")

def wolfram():
	try:
		url				= 'http://api.wolframalpha.com/v2/query?input='  +  urllib.quote( paramData )  + '&appid=' + apiKeys["wolfram"]
		hdr 			= {'User-Agent': 'Mozilla/5.0'} 
		request 		= urllib2.Request( url, headers=hdr)
		response 		= urllib2.urlopen( request)
		html			= response.read()
		res 			= re.findall('<plaintext>(.*?)</plaintext>', html )
		output 			= "\x02" + res[0] + "\x02 - " + res[1]
		irc.send("PRIVMSG " + channel + " :" + output + "\r\n") 
	except:
		irc.send("PRIVMSG " + channel + " :Sorry, i cannot find that.\r\n")


def imdb():
	try:
		url				= 'http://www.omdbapi.com/?t=' + paramData.replace(" ", "+")
		hdr 			= {'User-Agent': 'Mozilla/5.0'} 
		request 		= urllib2.Request( url, headers=hdr)
		response 		= urllib2.urlopen( request)
		html			= response.read()
		output 			= json.loads( html)

		link 			= "http://imdb.com/title/" + output["imdbID"]

		irc.send("PRIVMSG " + channel + " :\x02Found movie: " + output["Title"] + "\x02 - " + link + "\r\n")
	except:
		irc.send("PRIVMSG " + channel + " :Sorry, i cannot find that.\r\n")


def thanks():
	try:
		irc.send("PRIVMSG " + channel + " :You're welcome " + user + " :D\r\n")
	except:
		return 1

def join():
	for x in params:
		irc.send("JOIN " + x + "\r\n")


def leave():
	for x in params:
		irc.send("PART #" + x + "\r\n")


def weather():
	#http://api.openweathermap.org/data/2.5/weather?q=London,uk
	try:
		url				= 'http://api.openweathermap.org/data/2.5/weather?q=' + paramData.replace(" ", "+") + "&units=metric"
		hdr 			= {'User-Agent': 'Mozilla/5.0'} 
		request 		= urllib2.Request( url, headers=hdr)
		response 		= urllib2.urlopen( request)
		html			= response.read()
		output 			= json.loads( html)

		try:
			weather 		= output["weather"][0]["description"]
		except:
			irc.send("PRIVMSG " + channel + " :No weather info found for " + paramData + "\r\n")
			return 0

		windspeed 		= str( output["wind"]["speed"] ) + " km/h"

		try:
			windgust 		= "a gust of " +str( output["wind"]["gust"] ) + " km/h"
		except:
			windgust 		= "no gust"

		winddirection 	= output["wind"]["deg"]
		city 			= output["name"]

		if winddirection > 45 and winddirection < 135:
			winddirection	= "coming from the west" 
		if winddirection > 135 and winddirection < 225:
			winddirection 	= "coming from the north"
		if winddirection > 225 and winddirection < 315:
			winddirection	= "coming from the east"
		if winddirection > 315 and winddirection < 360:
			winddirection 	= "coming from the south"

		if city 		== "":
			city 		= output["sys"]["country"]

		temperature 	= output["main"]["temp"]
		humidity		= str( output["main"]["humidity"] ) + "%"

		irc.send("PRIVMSG " + channel + " :The weather in " + city + " : " + weather + ", with a temperature of " + str( temperature ) + " c ( " + str( temperature*9/5+32  ) + " F ) and a humidity of " + humidity  + ". The wind is " + winddirection + " at " + windspeed + " with " +  windgust  +  ".\r\n")
	except:
		irc.send("PRIVMSG " + channel + " :Could not find the weather for " + paramData + "\r\n")

def hug():
	irc.send("PRIVMSG " + channel + " :\x01ACTION Hugs " + user + "\x01\r\n")


def ahk():
	data 		= google_search("autohotkey: " + paramData)
	if data == "":
		irc.send("PRIVMSG " + channel + " :NO DATA FOUND\r\n")
	else:
		irc.send("PRIVMSG " + channel + " :" + data + "\r\n")

def rss():
	url				= 'http://ahkscript.org/boards/feed.php'
	hdr 			= {'User-Agent': 'Mozilla/5.0'} 
	request 		= urllib2.Request( url, headers=hdr)
	response 		= urllib2.urlopen( request)
	xml				= response.read()
	xml 			= xml.encode("utf-16")
	print( xml )

	xmlmatch 		= re.findall("<entry>.*?<author><name><.*?\[.*?\[(.*?)\]\]>.*?<updated>(.*?)<.*?<published>(.*?)</published>.*?<id>(.*?)</id>.*?<title.*?><.*?\[.*?\[(.*?)\]\]></title>", xml, re.S)
	
	i 				= 0

	output 			= ""

	while i < 5:
		name 			= xmlmatch[i][0]
		updated 		= xmlmatch[i][1]
		published 		= xmlmatch[i][2]
		link 			= HTMLParser.HTMLParser().unescape(xmlmatch[i][3])
		title 			= HTMLParser.HTMLParser().unescape(xmlmatch[i][4])

		print( title )
		irc.send( "PRIVMSG " + channel + " :" + name + " - " + title + " - " + link + "\r\n")
		i                       = i + 1


def message():
   	
	if reg.group("User") == botName:
		irc.send("PRIVMSG " + channel + " :Im not going to message myself, that would be stupid!\r\n")
		return 0

	messageData.append(user + "-" + reg.group("User") + "-" + paramData )


def bitcoin():
	try:
		url				= 'http://blockchain.info/ticker'
		hdr 			= {'User-Agent': 'Mozilla/5.0'} 
		request 		= urllib2.Request( url, headers=hdr)
		response 		= urllib2.urlopen( request)
		html			= response.read()
		output 			= json.loads( html)

		sellprice 		= output[paramData]['symbol'] + "" + str( output[paramData]['sell'] )
		payprice 		= output[paramData]['symbol'] + "" + str( output[paramData]['buy'] )
		irc.send("PRIVMSG " + channel + " :BlockChain bitcoin price for " + paramData + " - Sell price - " + sellprice + ", Buy price - " + payprice + "\r\n")
	except:
		irc.send("PRIVMSG " + channel + " :Cannot find the price for " + paramData + "\r\n")



def stop():
	sys.exit()

def commands():
	commandVar 		= ""

	for x in commandList:
		commandVar 	= commandVar + "" + x + " | "

	irc.send("PRIVMSG " + channel + " :Here is a list of commands: " + commandVar + "\r\n")
##################################################################################################################


##################################################################################################################
commandRegex 		= {
	".*" + bot_cmd + "(g|google|search)\s(?P<Data>.*?)(&{2}|\\r)": "google",
	".*" + bot_cmd + "(m|solve|math)\s(?P<Data>.*?)(&{2}|\\r)": "math",
	".*\s" + botName + "\s.*?(google|search)\s(?!(the\s|)(movie))(?P<Data>.*?)(&{2}|\\r)" : "google",
	".*" + bot_cmd + "(kill|k)\s(?P<Data>.*?)\s?(&{2}|\\r)" : "kill",
	".*\s" + botName + "\s.*?(kill)\s(?P<Data>.*?)\s?(&{2}|\\r)" : "kill",
	".*" + bot_cmd + "(wolfram|wa)\s(?P<Data>.*?)(&{2}|\\r)" : "wolfram",
	".*\s" + botName + "\s.*?(find (the)?|wolfram|what is (the))\s(?!(movie|weather))(?P<Data>.*?)(&{2}|\\r)" : "wolfram",
	".*" + bot_cmd + "(imdb|movie)\s(?P<Data>.*?)(&{2}|\\r)" : "imdb",
	".*\s" + botName + "\s.*?(movie|imdb)\s(?P<Data>.*?)(&{2}|\\r)" : "imdb",
	".*(?P<Data>(thanks?|fanks?|ty|tah?))(,|.)?\s?" + botName.lower() + "" : "thanks",
	".*\s" + botName + "\s.*?\s(?P<Data>(thanks?|fanks?|ty|tah?))\s.*" : "thanks",
	".*" + bot_cmd + "(join|j)\s(?P<Data>.*?)(&{2}|\\r)" : "join",
	".*" + bot_cmd + "(leave|l)\s(?P<Data>.*?)(&{2}|\\r)" : "leave",
	".*\s" + botName + "\s.*weather\s(like in|in)\s(?P<Data>.*?)(&{2}|\\r)" : "weather",
	".*" + bot_cmd + "(w|weather)\s(?P<Data>.*?)(&{2}|\\r)" : "weather",
	".*\s" + botName + "\s.*?(?P<Data>(gimme a hug|hug me|hug)).*?(&{2}|\\r)" : "hug",
	".*(?P<Data>(hug|hug me|gimme a hug)).*" + botName.lower() + ".*?(&{2}|\\r)" : "hug",
	".*\s" + botName + "\s.*(search ahk(\sfor)?|ahk search(\sfor)?)\s(?P<Data>.*?)(&{2}|\\r)" : "ahk",
	".*" + bot_cmd + "(ahk|a)\s(?P<Data>.*?)(&{2}|\\r)" : "ahk",
	".*\s" + botName + "\s.*?(?P<Data>(can you do|list of commands|command list))(&{2}|\\r)" : "commands",
	".*" + bot_cmd + "(?P<Data>(commands|c)\s?)(&{2}|\\r)" : "commands",
	".*" + bot_cmd + "(?P<Data>(stop|die)\s?)(&{2}|\\r)" : "stop",
	".*" + bot_cmd + "(?P<Data>(rss__|feed__)\s?)(&{2}|\\r)" : "rss",
	".*" + bot_cmd + "(message|msg)\s(?P<User>.*?)\s(?P<Data>.*?)\s?(&{2}|\\r)" : "message",
	".*" + bot_cmd + "(btc|bit|bitcoin)\s(?P<Data>.*?)\s?(&{2}|\\r)" : "bitcoin"
	
}

commandList 	= {
	"google" : google,
	"kill"	: kill,
	"wolfram" : wolfram,
	"imdb" : imdb,
	"thanks" : thanks,
	"join" : join,
	"leave" : leave,
	"weather" : weather,
	"hug" : hug,
	"ahk" : ahk,
	"commands" : commands,
	"stop" : stop,
	"rss" : rss,
	"message" : message,
	"bitcoin" : bitcoin,
	"math" : math
}

ownerCommands 		= ["join", "leave", "stop" ]

def callFunction(function):

	for key in ownerCommands:
		if key == function and host != master:
			irc.send("PRIVMSG " + channel + " :You are not my master!\r\n")
			return 0



	commandList[ function]()
##################################################################################################################


################################################## IRC STARTUP ###################################################
irc 				= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((network, port))

NICK 				= "NICK " + botName + " \r\n"
USER 				= "USER " + botName + " " + botName + " " + botName + " :Uptone Software\r\n"

irc.send( NICK )
irc.send( USER )

irc.send("PRIVMSG Nickserv :Identify sjBot " + password + " \r\n")

for x in content:
	irc.send("JOIN " + x + "\r\n")
##################################################################################################################

data 				= 1


while data:
	data 			= irc.recv(1024)
	dt 				= re.match(":(?P<User>.*?)!~?(?P<Host>.*?)\s(?P<Command>.*?)\s(?P<Channel>.*?)\s:(?P<Message>.*\\r)", data)


	if data[0:4] == "PING":											# If PING is found in the data.
		irc.send("PONG :" + data[6:] + " \r\n")	

	if dt:
		user 		= dt.group("User")
		host 		= dt.group("Host")
		command 	= dt.group("Command")
		channel 	= dt.group("Channel")


		message 	= dt.group("Message")


		for k in messageData:
			try:
				messplit 			= k.split('-')

				if messplit[1] == user:
					irc.send("PRIVMSG " + messplit[1] + " :" + messplit[1] + ", You have a message from " + messplit[0] + ": " + messplit[2] + "\r\n")
					messageData.remove(k)
			except:
				continue


		for x in commandRegex:
			reg 		= re.match(x, message, re.IGNORECASE)
			if reg:

				try:
					pm 			= reg.group("Pm")
					pm 			= 1
				except:
					pm 			= 0

				try:
					paramData 	= reg.group("Data")
					params 		= paramData.split(' ')
				except:
					paramData 	= reg.group("Cmd")
					params 		= paramData.split(' ')
				

				callFunction(commandRegex[x])
