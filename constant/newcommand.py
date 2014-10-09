import random
import os
import time

def execute(irc):
	while True:
		path 		= '/'.join( os.path.dirname(os.path.realpath(__file__)).split("/")[:-1] ) + "/plugins/"
		commands	= os.listdir(path)
		new 		= commands
		while commands == new:
			new 	= os.listdir(path )
			time.sleep(5)
		
		if len( new ) < len( commands ):
			irc.pMessage("__all__", "Command has been removed: " + ' '.join( list(set( commands) - set( new ) ) ) )
		if len( new ) > len( commands ):
			irc.pMessage("__all__", "Command has been added: " + ' '.join( list( set(new) - set( commands ) ) ) )
