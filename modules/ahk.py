import urllib2
import urllib
import json

try: 
	search 			= urllib.quote( str("site:autohotkey.com " + self.paramData ))

	url			= 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=' + search 
	hdr 			= {'User-Agent': 'Mozilla/5.0'} 
	request 		= urllib2.Request( url, headers=hdr)
	response 		= urllib2.urlopen( request)

	html			= response.read()
	output 			= json.loads( html)

	title 			= output['responseData']['results'][0]['titleNoFormatting']
	url 			= output['responseData']['results'][0]['url']

	url 			= urllib.unquote( url).encode('utf-8')
	title 			= urllib.unquote( title).encode('utf-8')

	output 		= "\x02" + title + "\x02 - " + url
except IndexError:
	output 		= "\x02\x035No data found\x02\x03"
