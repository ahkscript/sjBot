import urllib.request
import html.parser
import time
import re

def urlDownload( url ):
		try:
			response 	= urllib.request.urlopen(url) 
		except UnicodeEncodeError:
			return "Aww maaaaaan. I ran into some jank characters there. Decode error, sorry :P"
		except:
			return "__notext__"

		return response.read().decode('utf-8')


def execute(irc):
	while True:
		data 		= urlDownload("http://ahkscript.org/boards/feed.php")
		find 		= re.findall("<entry>.*?<author>.*?<name>.*?<!\[CDATA\[(.*?)\].*?<updated>(.*?)</.*?published>(.*?)</.*?id>(.*?)</.*?title type.*?<!\[.*?\[(.*?)\]", data, re.S )
		old 		= find[0][0] + ": " + find[0][4] + " - " + html.parser.HTMLParser().unescape( find[0][3] )
		new 		= old

		while old == new:
			time.sleep(20)
			data 		= urlDownload("http://ahkscript.org/boards/feed.php")
			find 		= re.findall("<entry>.*?<author>.*?<name>.*?<!\[CDATA\[(.*?)\].*?<updated>(.*?)</.*?published>(.*?)</.*?id>(.*?)</.*?title type.*?<!\[.*?\[(.*?)\]", data, re.S )
			new 		= find[0][0] + ": " + find[0][4] + " - " + html.parser.HTMLParser().unescape( find[0][3] )

		irc.pMessage(["#ahkscript","#Sjc_Bot"], new )
