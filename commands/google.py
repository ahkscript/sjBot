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

			with open('commands/more.search', 'w') as more:
				more.write(htmlData)

			response = json.loads( htmlData )
			print( response )
			title = response['responseData']['results'][0]['titleNoFormatting']
			url = response['responseData']['results'][0]['url']

		except IndexError:
			return ['No data found!']
		return ["\x02" + parent.html_decode( title ) + "\x02 - " + parent.shorten_url(url)]
