import random
metaData 	= { "help": ["This command says hello to a user.", "Usage: &botcmdhelp [command name]"], "aliases": ["hello", "hey"], "owner": 0 }


def execute(command, user, host, channel, params):	
		if len( params ) > 0:
			user 	= params[0]
		responses 	= ["Hi there " + user, "Hey " + user + " :D", "Hiii " + user, "Hawwt daamn, Hi " + user + " :)"]	
		return random.choice( responses )
