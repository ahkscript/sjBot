import random

colorCode 	= [ "\x032", "\x033","\x034", "\x035", "\x036", "\x037","\x038", "\x039","\x0310","\x0311","\x0312","\x0313","\x0315" ]
data 		= ""
texts 		= ["Danceroo! Yay, yay, YAAAAAYYY! \(^_^)/ :D", "Lets dance " + self.user + " :D. \o\ /o/ \o/", "Swweeet dance time \(^_^)/ :D :D :D"]


text 		= random.choice( texts )

for k in text.split(" "):
	data 	= data + random.choice(colorCode) + k + "\x03 "

output 		= data
