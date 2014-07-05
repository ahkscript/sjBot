params 		= self.fullData
output 		= ""

print( params )

if len( params ) == 0:
	output 		= "Here is a list of commands"
	for commands in self.ontextObject["commands"]:
		if self.ontextObject["commands"][commands]["owner"] == 1:
			output 		= output + " | \x02" + commands + "\x02" 
		else:
			output 		= output + " | " + commands  
else:

	for c in self.ontextObject["commands"]:
		if any( v == self.fullData[0]  for v in self.ontextObject["commands"][c]["cmd"] ):
			output 		= self.ontextObject["commands"][c]["help"]
