meta_data = {"help": ["This command makes sjBot say stuff.", "Usage: &botcmdsay <message>"], "aliases": ['say'], "owner": 0 }

def execute(parent, commands, user, host, channel, params):
	if len(params) == 0:
		return [meta_data['help'][0]]
	if params[0] == '*action*':
		return ['\x01ACTION ' + ' '.join(params[1:]) + '\x01']
	return [' '.join(params)]
