import random
meta_data 	= { "help": ["Kills a person with a weapon.","Usage: &botcmdkill <person> [weapon]"], "aliases": ["k", "kill"], "owner": 0 }


def execute(parent, commands, user, host, channel, params ):
	weapons 		= [	"a small lion.",
						"a dictionary",
						"an angry mountain.",
						"the power of 3.",
						"a honey badger.",
						"a Hyper beam.",
						"a short drop and a sudden stop.",
						"a spoon, because knives are too easy.",
						"a bowtie.",
						"tlm.",
						"a rraaaiiinnboww trout.",
						"bordem."
					  ]		



	if len( params ) == 0:
		return {'Status': -1, 'Text': "This command needs more params", 'Error': 'Needs more params'}

	if len( params ) < 2:
		weapon 		= random.choice( weapons )
	else:
		weapon 		= ' '.join( params[1:] )

	user 		= params[0]


	return ['\x01ACTION Kills ' + str( user ) + " with " + weapon + '\x01']
