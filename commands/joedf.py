import random
meta_data 	= { "help": ["joedf"], "aliases": ["joedf", "jd", "flip"], "owner": 0 }


faces 		= ["(╯°□°)╯", "(╯⌐■_■)╯", "(╯•_•)╯"]
chars = list('ɐqɔpǝɟƃɥᴉɾʞlɯuodbɹsʇnʌʍxʎz∀qƆpƎℲפHIſʞ˥WNOԀQɹS┴∩ΛMX⅄ZƖᄅƐㄣϛ9ㄥ860-=¡@#$%^⅋*)(‾+><¿ ')
normal = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-=!@#$%^&*()_+<>? ')

def execute(parent, commands, irc, user, host, channel, params):
	if len(params) > 0:
		return [random.choice( faces ) + '︵ ' +''.join([chars[normal.index(x)] for x in ''.join(params)])]
	return [random.choice( faces ) + "︵ ┻━┻"]
