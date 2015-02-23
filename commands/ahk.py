import urllib.request
import json
import html.parser
import os
import difflib
import sys

meta_data = { "help": ["Searches google for an ahk related query.","Usage: &botcmdahk <query>"], "aliases": ["ahks", "search", "ahk", "a"], "owner": 0 }


#https://www.googleapis.com/customsearch/v1?key=AIzaSyAJQbRWt3p4S5sAiHL_iiot87KcbEa0dsQ&cx=009062493091172133168:_o2f4moc9ce&q=
def execute(parent, commands, irc, user, host, channel, params):
	
	with open(os.path.dirname(os.path.realpath(__file__)) + '/docs.json', 'r') as docs:
		docdata = json.loads(docs.read())

	matches = difflib.get_close_matches(' '.join( params ).lower(), docdata )
	if len( matches ) > 0:
		return ["\x02" + matches[0] + "\x02 - " + parent.shorten_url(docdata[matches[0]])]

	try:
		if len( params ) == 0:
			return ['Need more params','Usage: &botcmdahk <query>']
		
		search 		= '%20'.join( params ).replace("\r\n", "")
		
		try:
			htmlData 	= parent.download_url( 'https://www.googleapis.com/customsearch/v1?key=AIzaSyAJQbRWt3p4S5sAiHL_iiot87KcbEa0dsQ&cx=009062493091172133168:_o2f4moc9ce&q=' + search )
		except UnicodeDecodeError:
			return {'Status': 0,'Text': 'No data found!', 'Error': 'No Error'}

		response = json.loads( htmlData )
		title = response['items'][0]['title']
		url = response['items'][0]['link']

	except IndexError:
		return ['No data found!']
	return ["\x02" + urllib.parse.unquote( title ) + "\x02 - " + parent.shorten_url(url)]
