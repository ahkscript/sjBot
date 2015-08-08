import urllib.request
import json
import html.parser
import os
import difflib
import sys

meta_data = { "help": ["Searches google for a donation coder related query.","Usage: &botcmddc <query>"], "aliases": ["donationcoder", "dc"], "owner": 0 }



def execute(parent, commands, user, host, channel, params):

	try:
		if len( params ) == 0:
			return ['Need more params','Usage: &botcmddc <query>']
		
		search 		= '%20'.join( params ).replace("\r\n", "")
		
		try:
			htmlData 	= parent.download_url( 'https://www.googleapis.com/customsearch/v1?key=AIzaSyAJQbRWt3p4S5sAiHL_iiot87KcbEa0dsQ&cx=009062493091172133168:xwjfsl5agjc&q=' + search )
		except UnicodeDecodeError:
			return ['No data found!']

		with open('commands/more.search', 'w') as more:
			more.write(htmlData)

		response = json.loads( htmlData )
		title = response['items'][0]['title']
		url = response['items'][0]['link']
		url = url.replace(';wap2', '')
		url = url.replace(';wap', '')

	except (IndexError, KeyError):
		return ['No data found!']
	return ["\x02" + urllib.parse.unquote( title ) + "\x02 - " + parent.shorten_url(url)]
