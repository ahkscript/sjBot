import urllib.request
import json


meta_data   = { "help": ["Returns a definition of a specified word.","Usage: &botcmddefine <word>"], "aliases": ["def", 'dict', 'define'], "owner": 0 }


def execute(parent, commands, user, host, channel, params):
    params = [urllib.parse.quote(x) for x in params]
    if len(params) == 0:
        return ['This command needs more params']
    js = parent.download_url('http://api.wordnik.com/v4/word.json/' + '%20'.join(params).lower() +'/definitions?limit=200&includeRelated=true&useCanonical=false&includeTags=false&api_key=a2a73e7b926c924fad7001ca3111acd55af2ffabf50eb4ae5')
    data = json.loads(js)
    try:
        return ['\x02' + data[0]['word'] + '\x02 - ' + data[0]['text']]
    except Exception:
        return 'Could not find that.'
