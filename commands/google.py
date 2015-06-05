import urllib.request
import json
import html.parser
meta_data 	= { "help": ["Searches google for a query.","Usage: &botcmdgoogle <query>"], "aliases": ["google", "g", "search"], "owner": 0 }


def execute(parent, commands, user, host, channel, params):
		try:		
			if len( params ) == 0:
				return [meta_data['help'][1]]
			search 		= '%20'.join( params ).replace("\r\n", "")
			try:
				htmlData 	= parent.google(search)
			except UnicodeDecodeError:
				return ['No data found!']

			with open('more.search', 'r') as more:
				more.write(htmlData)
			response = json.loads( htmlData )
			title = response['items'][0]['title']
			url = response['items'][0]['link']

		except IndexError:
			return ['No data found!']
		return ["\x02" + urllib.parse.unquote( title ) + "\x02 - " + parent.shorten_url(url)]
