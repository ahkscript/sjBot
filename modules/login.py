import hashlib

output 			= ""

if len( self.fullData ) < 1:
	output 		= "Please use more params for this command."
elif len( self.fullData ) < 0:
	output 		= "Please use params for this command."
else:
	user 		= self.fullData[0]
	password 	= self.fullData[1]
	
	for x in self.ownerlist:
		if x[0] == user.lower():
			
			if hashlib.sha224( password ).hexdigest() == x[1].lower():
				if any( self.host == c for c in self.owners ):
					output 		= "You are already logged in as " + user	
				else:
					self.owners.append(self.host)
					owners 		= self.owners
					output 		= "Logged in as " + user
			else:
				output 		= "Could not login!"
