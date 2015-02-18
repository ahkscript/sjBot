import urllib.request
import json
import html.parser
meta_data 	= { "help": ["Searches google for a query.","Usage: &botcmdgoogle <query>"], "aliases": ["google", "g", "search"], "owner": 0 }


def execute(parent, command, user, host, channel, params):
		try:		
		
			if len( params ) == 0:
				return {'Status': -1, 'Text': meta_data['help'][1], 'Error': "This command needs more params"}
		
			search 		= '%20'.join( params ).replace("\r\n", "")
		#https://www.googleapis.com/customsearch/v1?key=AIzaSyAJQbRWt3p4S5sAiHL_iiot87KcbEa0dsQ&cx=009062493091172133168:4ckmchbpuzy&q=
			try:
				htmlData 	= parent.download_url( "https://www.googleapis.com/customsearch/v1?key=AIzaSyAJQbRWt3p4S5sAiHL_iiot87KcbEa0dsQ&cx=009062493091172133168:4ckmchbpuzy&q=" + search)
			except UnicodeDecodeError:
				return {'Status': 0, 'Text': "No data found!", 'Error': 'No Error'}

			response = json.loads( htmlData )
			title = response['items'][0]['title']
			url = response['items'][0]['link']

		except IndexError:
			return {'Status': 0, 'Text': "No data found!", 'Error': 'No Error'}
		return {'Status': 0, 'Text': "\x02" + urllib.parse.unquote( title ) + "\x02 - " + command[5].shorten_url(url), 'Error': 'No Error'}
