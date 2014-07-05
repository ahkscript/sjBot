if len( self.fullData ) < 0:
	output 		= "Please specify the channels to join."

for x in self.fullData:
	self.irc.send("JOIN " + x + "\r\n")

output 			= "__notext__"
