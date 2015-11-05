meta_data 	= { "help": ["Gives help on commands.","Usage: &botcmdhelp [command name]"], "aliases": ["help", "shelp"], "owner": 0 }

def execute(parent, commands, user, host, channel, params ):
	output = []

	if len( params ) > 0:
		if params[0] == 'all':
			pass
		for z in commands:
			if any( params[0] == cmd for cmd in commands[z].meta_data["aliases"]):
				if channel == '##monsterhunter' or len(commands[z].meta_data["help"]) > 2:
					return ['PM'] + commands[z].meta_data["help"]
				return commands[z].meta_data["help"]
			else:
				continue

	cmds = []
	for x in commands:
		print( hasattr(commands[x], 'channel_specific') )
		if hasattr(commands[x], 'channel_specific'):
			if channel not in commands[x].channel_specific and 'all' not in params:
				continue
		if hasattr(commands[x], 'dont_show'):
			if channel in commands[x].dont_show and 'all' not in params:
				continue
		if hasattr(commands[x], 'show'):
			if len(params) > 0 and params[0] == 'all':
				pass
			elif commands[x].show == False:
				continue
		cmds.append(x)
	if channel == '##monsterhunter':
		return ['PM', "Please use &botcmdhelp [command name], for more info.", "Here is a list of commands. " + ", ".join(sorted(cmds)) + "."]
	return ["Please use &botcmdhelp [command name], for more info.", "Here is a list of commands. " + ", ".join(sorted(cmds)) + "."]