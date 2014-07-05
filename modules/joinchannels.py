for channel in self.channelList:
	self.irc.send("JOIN " + channel + "\r\n")

output 		= "__notext__"
