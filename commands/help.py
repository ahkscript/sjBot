meta_data 	= { "help": ["Gives help on commands.","Usage: &botcmdhelp [command name]"], "aliases": ["help", "shelp"], "owner": 0 }


def execute(parent, commands, irc, user, host, channel, params ):
	output = []

	if len( params ) > 0:
		for z in commands:
			if any( params[0] == cmd for cmd in commands[z].meta_data["aliases"]):
				return commands[z].meta_data["help"]
			else:
				continue
	
	return ["Please use &botcmdhelp [command name], for more info.", "Here is a list of commands. " + ", ".join(sorted(commands)) + "."]
