import urllib2
import urllib
import json
import re
import HTMLParser
import sys

output 		= ""

params 		= self.fullData
print( params )
try:
	number 			= int( params[0] )
except IndexError:
	number 			= 5
except ValueError:
	output 			= "Please use a number for this paramater."

if output == "":
		
	if len( params ) > 1:
		self.channel 	= params[1]

	if number > 10:
		number 		= 10

	url				= 'http://ahkscript.org/boards/feed.php'
	hdr 			= {'User-Agent': 'Mozilla/5.0'} 
	request 		= urllib2.Request( url, headers=hdr)
	response 		= urllib2.urlopen( request)
	xml				= response.read()
	xml 			= unicode(xml, errors='ignore')

	xmlmatch 		= re.findall("<entry>.*?<author><name><.*?\[.*?\[(.*?)\]\]>.*?<updated>(.*?)<.*?<published>(.*?)</published>.*?<id>(.*?)</id>.*?<title.*?><.*?\[.*?\[(.*?)\]\]></title>", xml, re.S)
		
	i 				= 0

	output 			= ""

	while i < number:
		name 			= xmlmatch[i][0]
		updated 		= xmlmatch[i][1]
		published 		= xmlmatch[i][2]
		link 			= HTMLParser.HTMLParser().unescape(xmlmatch[i][3])
		title 			= HTMLParser.HTMLParser().unescape(xmlmatch[i][4])

		output 			= output + "\rPRIVMSG " + self.channel + " :" + title + " - " + name + " : " + link
		print( output )	
		i                       = i + 1
