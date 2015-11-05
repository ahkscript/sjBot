import random
meta_data 	= { "help": ["joedf"], "aliases": ["joedf", "jd", "flip"], "owner": 0 }


faces 		= ["(╯°□°)╯", "(╯⌐■_■)╯", "(╯•_•)╯"]
chars = list('ɐqɔpǝɟƃɥᴉɾʞlɯuodbɹsʇnʌʍxʎz∀qƆpƎℲפHIſʞ˥WNOԀQɹS┴∩ΛMX⅄ZƖᄅƐㄣϛ9ㄥ860-=¡@#$%^⅋*)(‾+><¿ ')
normal = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890-=!@#$%^&*()_+<>? ')

def execute(parent, commands, user, host, channel, params):
	if len(params) > 0:
		text = ' '.join(params)
		for char in text:
			if char == ' ':
				continue
			if char in chars:
				text = text.replace(char, normal[chars.index(char)])
			if char in normal:
				text = text.replace(char, chars[normal.index(char)])
		text = [x for x in text]
		text.reverse()
		return [random.choice( faces ) + '︵ ' + ''.join(text)]
			
	return [random.choice( faces ) + "︵ ┻━┻"]
