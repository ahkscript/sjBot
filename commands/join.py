meta_data 	= { "help": ["Makes the bot join a channel. Only usable by one of the bots owners.","Usage: &botcmdjoin <channel 1> [channel 2] [channel 3]"], "aliases": ["j", "join"], "owner": 1 }


def execute(parent, command, user, host, channel, params ):
	parent.irc.join( params )
	return 0
