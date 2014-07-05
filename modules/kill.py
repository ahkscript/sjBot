import random

weapon 		= ""
params 		= self.fullData

if len( params ) > 1:
	for k in params[1:]:
		weapon 	= weapon + k + " "
else:
	weapon 		= random.choice( self.weapons )
			

if len(params ) > 0:
	killWho 	= params[0]
else:
	output 		= "I require more params for this command."


output 		= "\x01ACTION Kills " + killWho + " with " + weapon + "\x01"
