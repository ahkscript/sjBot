import socket

self.irc 		= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
self.irc.connect((self.network, self.port))
self.irc.send("NICK " + self.botName + " \r\n")
self.irc.send("USER " + self.botName + " " + self.botName + " " + self.botName + " :Uptone Software\r\n")
self.irc.send("PRIVMSG NickServ :Identify " + self.botName + " " + self.password + "\r\n")		

output 		= "__notext__"
