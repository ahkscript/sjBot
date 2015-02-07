import urllib.request
import json
import html.parser
metaData 	= { "help": ["Searches google for a query.","Usage: &botcmdgoogle <query>"], "aliases": ["google", "g", "search"], "owner": 0 }


def urlDownload( url ):
		try:
			response 	= urllib.request.urlopen(url) 
		except UnicodeEncodeError:
			return "Aww maaaaaan. I ran into some jank characters there. Decode error, sorry :P"
		except:
			return "__notext__"

		return response.read().decode('utf-8')


def execute(command, user, host, channel, params):
		try:		
		
			if len( params ) == 0:
				return ["This command needs more params"]
		
			search 		= '%20'.join( params ).replace("\r\n", "")
		
			htmlData 	= urlDownload( "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=" + search + "&cx=009062493091172133168:4ckmchbpuzy" )

		
			if htmlData == "__notext__":
				return ["No data found!"]

			response	= json.loads( htmlData )
			title 		= html.parser.HTMLParser().unescape( response["responseData"]["results"][0]["titleNoFormatting"] )
			url 		= html.parser.HTMLParser().unescape( urllib.parse.unquote( response["responseData"]["results"][0]["url"] ) )

		except IndexError:
			return ["No data found!"]
		return [urllib.parse.unquote( title ) + " - " + url]
