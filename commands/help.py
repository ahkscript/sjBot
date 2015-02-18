meta_data 	= { "help": ["Gives help on commands.","Usage: &botcmdhelp [command name]"], "aliases": ["help", "shelp"], "owner": 0 }


def execute(parent, commands, user, host, channel, params ):
	output = []

	if len( params ) > 0:
		for z in commands:
			if any( params[0] == cmd for cmd in commands[z].meta_data["aliases"]):
				return {'Status': 0, 'Text': commands[z].meta_data["help"], 'Error': 'No Error'}
			else:
				continue
	
	return {'Status': 0, 'Text': ["Please use " + parent.botcmd + "help [command name], for more info.", "Here is a list of commands. " + ", ".join(sorted(commands)) + "."], 'Error': 'No Error'}
