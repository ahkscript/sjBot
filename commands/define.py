import urllib.request
import json
meta_data 	= { "help": ["Returns a definition of a specified word.","Usage: &botcmddefine <word>"], "aliases": ["def", 'dict', 'define'], "owner": 0 }

#http://api.wordnik.com/v4/word.json/food/definitions?limit=200&includeRelated=true&useCanonical=false&includeTags=false&api_key=a2a73e7b926c924fad7001ca3111acd55af2ffabf50eb4ae5

def execute(parent, commands, irc, user, host, channel, params ):
	if len(params) == 0:
		return {'Status': -1, 'Text': meta_data['help'][1], 'Error': 'This command needs more params'}

	js = parent.download_url('http://api.wordnik.com/v4/word.json/' + '%20'.join(params) +'/definitions?limit=200&includeRelated=true&useCanonical=false&includeTags=false&api_key=a2a73e7b926c924fad7001ca3111acd55af2ffabf50eb4ae5')
	data = json.loads(js)
	return ['\x02' + data[0]['word'] + '\x02 - ' + data[0]['text']]
