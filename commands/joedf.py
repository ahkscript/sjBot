import random
meta_data 	= { "help": ["joedf"], "aliases": ["joedf", "jd", "flip"], "owner": 0 }


faces 		= ["(╯°□°)╯", "(╯⌐■_■)╯", "(╯•_•)╯"]

def execute(parent, command, user, host, channel, params ):
	return {'Status': 0, 'Text': random.choice( faces ) + "︵ ┻━┻", 'Error': 'No Error'}
