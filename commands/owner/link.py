import json
import os

meta_data = { "help": ["Adds a link to the list of doc links.","Usage: &botcmdlink <name> <link>"], "aliases": ["link", "addlink"], "owner": 1 }

def execute(parent, commands, user, host, channel, params):
	if len(params) < 2:
		return [meta_data['help'][1]]
	with open(parent.def_dir + '/commands/docs.json', 'r') as docs:
		docdata = json.loads(docs.read())
	query = ' '.join(params[:params.index('|')])
	link = params[params.index('|') + 1]
	if query in docdata:
		return ['This is already in the link list!']
	docdata[query] = link
	output = json.dumps(docdata)
	with open(parent.def_dir + '/commands/docs.json', 'w') as my_file:
		my_file.write(output)
	return [query + " added to the list."]
