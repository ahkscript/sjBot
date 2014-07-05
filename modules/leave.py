if len( self.fullData ) < 0:
	output 		= "Please specify the channels to leave."

for x in self.fullData:
	self.irc.send("PART " + x + "\r\n")

output 			= "__notext__"
