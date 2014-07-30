params 		= self.fullData
oData 		= ""

print( params )

if len( params ) == 0:
	oData		= "Here is a list of commands"
	for commands in self.commands:
		if self.commands[commands]["owner"] == 1 and not any( c == self.host  for c in self.owners ):
			continue
		else:
			oData 		= oData + " | " + commands
else:

	for c in self.commands:
		if any( v == self.fullData[0]  for v in self.commands[c]["cmd"] ):
			oData 		= self.commands[c]["help"]

output 		= {"text": oData, "channel": "__default__"}
