if len( self.fullData ) < 0:
	output 		= "Please specify a nickname to change to."	
else:
	self.irc.send("NICK " + self.fullData[0] + " \r\n")
	self.botName 	= self.fullData[0]
	output 		= "__notext__"
