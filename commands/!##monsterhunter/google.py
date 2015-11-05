import urllib.request
import json
import html.parser


meta_data   = { "help": ["Searches google for a query.","Usage: &botcmdgoogle <query>"], "aliases": ["google", "g", "search"], "owner": 0 }


def execute(parent, commands, user, host, channel, params):
    params = [urllib.parse.quote(x) for x in params]
    try:        
        if len( params ) == 0:
            return [meta_data['help'][1]]
        search      = '%20'.join( params ).replace("\r\n", "")
        try:
            htmlData    = parent.google(search)
        except UnicodeDecodeError:
            return ['No data found!']

        response = json.loads( htmlData )
        more = []
        for k, item in enumerate(response['responseData']['results']):
            if k == 0:
                continue
            more.append({'title': item['titleNoFormatting'], 'url': item['url']})
        with open(parent.def_dir + '/commands/more.json', 'w') as mfile:
            mfile.write(json.dumps(more))
        title = response['responseData']['results'][0]['titleNoFormatting']
        url = response['responseData']['results'][0]['url']

    except IndexError:
        return ['No data found!']
    return ["\x02" + parent.html_decode( title ) + "\x02 - " + parent.shorten_url(url)]
