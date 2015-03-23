meta_data 	= { "help": ["Makes the bot leave a channel. Only usable by one of the bots owners.","Usage: &botcmdleave <channel 1> [channel 2] [channel 3]"], "aliases": ["l", "leave"], "owner": 1 }


def execute(parent, command, user, host, channel, params ):
	for channel in params:
		parent.leave( channel )
	return 0
