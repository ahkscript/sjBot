import json
import os

meta_data = { "help": ["Adds a link to the list of doc links.","Usage: &botcmdlink <name> <link>"], "aliases": ["link", "addlink"], "owner": 1 }

def execute(parent, command, user, host, channel, params):
	if len(params) < 2:
		return {'Status': -1, 'Text': meta_data['help'][1], 'Error': 'This command needs more params'}
	with open(os.path.dirname(os.path.realpath(__file__)) + '/docs.json', 'r') as docs:
		docdata = json.loads(docs.read())
	query = ' '.join(params[:params.index('|')])
	link = params[params.index('|') + 1]
	if query in docdata:
		return {'Status': 0, 'Text': "This is already in the link list!", 'Error': 'No Error'}
	docdata[query] = link
	output = json.dumps(docdata)
	with open(os.path.dirname(os.path.realpath(__file__)) + '/docs.json', 'w') as my_file:
		my_file.write(output)
	return {'Status': 0, 'Text': query + " added to the list.", 'Error': 'No Error'}
