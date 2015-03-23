import urllib.request
import json
import html.parser
meta_data 	= { "help": ["Searches google for a query.","Usage: &botcmdgoogle <query>"], "aliases": ["google", "g", "search"], "owner": 0 }


def execute(parent, commands, user, host, channel, params):
		try:		
		
			if len( params ) == 0:
				return [meta_data['help'][1]]
		
			search 		= '%20'.join( params ).replace("\r\n", "")
		#https://www.googleapis.com/customsearch/v1?key=AIzaSyAJQbRWt3p4S5sAiHL_iiot87KcbEa0dsQ&cx=009062493091172133168:4ckmchbpuzy&q=
			try:
				htmlData 	= parent.download_url( "https://www.googleapis.com/customsearch/v1?key=AIzaSyAJQbRWt3p4S5sAiHL_iiot87KcbEa0dsQ&cx=009062493091172133168:4ckmchbpuzy&q=" + search)
			except UnicodeDecodeError:
				return ['No data found!']

			response = json.loads( htmlData )
			title = response['items'][0]['title']
			url = response['items'][0]['link']

		except IndexError:
			return ['No data found!']
		return ["\x02" + urllib.parse.unquote( title ) + "\x02 - " + parent.shorten_url(url)]
