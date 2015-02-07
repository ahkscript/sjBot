import urllib.request
import json
import html.parser
import os
import difflib

metaData = { "help": ["Searches google for an ahk related query.","Usage: &botcmdahk <query>"], "aliases": ["ahks", "search", "ahk", "a"], "owner": 0 }


def urlDownload( url ):
	try:
		response 	= urllib.request.urlopen(url) 
	except UnicodeEncodeError:
		return "Aww maaaaaan. I ran into some jank characters there. Encode error, bro :P"
	except:
		return "__notext__"

	return response.read().decode('utf-8')

#https://www.googleapis.com/customsearch/v1?key=AIzaSyAJQbRWt3p4S5sAiHL_iiot87KcbEa0dsQ&cx=009062493091172133168:_o2f4moc9ce&q=
def execute(command, user, host, channel, params):
	with open(os.path.dirname(os.path.realpath(__file__)) + '/docs.json', 'r') as docs:
		docdata = json.loads(docs.read())

	matches = difflib.get_close_matches(' '.join( params ).lower(), docdata )
	if len( matches ) > 0:	
		return [ "\x02" + matches[0] + "\x02 - " + docdata[matches[0]] ]

	try:		
		
		if len( params ) == 0:
			return ["This command needs more params"]
		
		search 		= '%20'.join( params ).replace("\r\n", "")
		
		htmlData 	= urlDownload( 'https://www.googleapis.com/customsearch/v1?key=AIzaSyAJQbRWt3p4S5sAiHL_iiot87KcbEa0dsQ&cx=009062493091172133168:_o2f4moc9ce&q=' + search )

		
		if htmlData == "__notext__":
			return ["No data found!"]

		response = json.loads( htmlData )
		title = response['items'][0]['title']
		url = response['items'][0]['link']

	except IndexError:
		return ["No data found!"]
	return [ "\x02" + urllib.parse.unquote( title ) + "\x02 - " + url]
