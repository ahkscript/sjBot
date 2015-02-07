metaData 	= { "help": ["Gives help on commands.","Usage: &botcmdhelp [command name]"], "aliases": ["help", "shelp"], "owner": 0 }


def execute(command, user, host, channel, params ):
	commands 		= command[1]
	output 			= []
	
	if command[3] == 1:
		for x in commands:
			if commands[x].metaData["owner"] == 1:
				commands.remove(x)
	
	if len( params ) > 0:
		for z in commands:
			if any( params[0] == cmd for cmd in commands[z].metaData["aliases"]):
				return commands[z].metaData["help"]
			else:
				return "Command not found"
	
	return ["Please use " + command[2][0] + "help [command name], for more info.", "Here is a list of commands. " + ", ".join(sorted(commands)) + "."]
