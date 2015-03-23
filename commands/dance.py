import random
meta_data 	= { "help": ["Dances","Usage: &botcmddance"], "aliases": ["dance", "d"], "owner": 0 }



def execute(parent, commands, user, host, channel, params ):
	dance  		= ["<(^_^)>",">(^_^)>","<(^_^)<","^(^_^)^","v(^_^)v"]
	colorCode 	= [ "\x032", "\x033","\x034", "\x035", "\x036", "\x037","\x038", "\x039","\x0310","\x0311","\x0312","\x0313","\x0315" ]
	returnData 	= []

	for x in range(3, 10):
		returnData.append( random.choice( colorCode ) + random.choice( dance ) + "\x03" )

	return ['Wooo dance time! ' + ' '.join( returnData )]
