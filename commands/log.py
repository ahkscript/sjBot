#!/usr/bin/env python3


meta_data 	= { "help": ["Outputs the log to a file. Only usable by the bots owner."], "aliases": ["log", "l"], "owner": 1 }


def execute(parent, commands, user, host, channel, params):
	with open(parent.def_dir + '/log', 'w') as log:
		for x in parent.log:
			log.write(x.decode('utf-8'))
	return ['Output complete.']