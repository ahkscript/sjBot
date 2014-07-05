import random

if len( self.fullData ) > 0:
	user 		= self.fullData[0]
else:
	user 		= self.user

possible 	= ["shhh, there there.", "suck it up, sissy pants.","its okay. &botname is here.", "don't worry bro! I believe at you."] 
output 		= "\x01ACTION hugs " + user + " and whispers '" + random.choice( possible ) + "'\x01"
