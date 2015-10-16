import json
import urllib.parse

meta_data 	= { "help": ["Searches for a wiki page","Usage: &botcmdwiki <query>"], "aliases": ["wiki", "wik"], "owner": 0 }

def execute(parent, commands, user, host, channel, params):
	if len(params) == 0:
		return [meta_data['help'][1]]
	
	search = 'site:http://en.wikipedia.org%20' + '%20'.join(params)
	print( search )
	try:
		search_data = parent.download_url('https://www.googleapis.com/customsearch/v1?key=A' + parent.keys['google'] + 'Q&cx=009062493091172133168:4ckmchbpuzy&q=' + search)
	except UnicodeDecodeError:
		return ['No data found!']
	
	response = json.loads(search_data)
	try:
		title = response['items'][0]['title']
		url = response['items'][0]['link']
	except (IndexError, KeyError):
		return ['No data found!']
	return ["\x02" + urllib.parse.unquote( title ) + "\x02 - " + parent.shorten_url(url)]
