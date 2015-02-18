import random
meta_data 	= { "help": ["This command says hello to a user.", "Usage: &botcmdhelp [command name]"], "aliases": ["hello", "hey", "hi"], "owner": 0 }


def execute(parent, command, user, host, channel, params):	
		if len( params ) > 0:
			user 	= params[0]
		responses 	= ["Hi there " + user, "Hey " + user + " :D", "Hiii " + user, "Hawwt daamn, Hi " + user + " :)"]	
		return {'Status': 0, 'Text': random.choice( responses ), 'Error': 'No Error'}
