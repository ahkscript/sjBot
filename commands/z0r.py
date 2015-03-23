import random

meta_data = { "help": ["Returns a random or specified gif from z0r.de","Usage: &botcmdz0r [number]"], "aliases": ["z0r", "zor",'z'], "owner": 0 }

def execute(parent, commands, user, host, channel, params):
	limit = 6774
	if len(params) > 0:
		number = params[0]
	else:
		number = random.choice(range(0,limit))

	return ['http://z0r.de/L/z0r-de_' + str(number) + '.swf']
