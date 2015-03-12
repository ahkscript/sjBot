#!/urs/bin/env python3
import time

generated = ['\033[{}m'.format(str(i)) for i in range(0,99)]

colors = {'end': generated[0],
	'error': generated[1],
	'italic': generated[3],
	'underline': generated[4],
	'strike': generated[9],
	'dblack': generated[30],
	'dred': generated[31],
	'dgreen': generated[32],
	'dyellow': generated[33],
	'dblue': generated[34],
	'dpurple': generated[35],
	'dteal': generated[36],
	'dwhite': generated[37],
	'_black': generated[40],
	'_red': generated[41],
	'_green': generated[42],
	'_yellow': generated[43],
	'_blue': generated[44],
	'_purple': generated[45],
	'_teal': generated[46],
	'_white': generated[47],
	'black': generated[90],
	'red': generated[91],
	'green': generated[92],
	'yellow': generated[93],
	'blue': generated[94],
	'purple': generated[95],
	'teal': generated[96],
	'white': generated[97] }

def pprint(data, color=None, background=None, prefix='', suffix='\r\n', timestamp=0, timecolor='purple'):
	if timestamp:
		time_object = time.localtime(time.time())
		tcolor = colors[timecolor]
		print('{}[{:0>2}:{:0>2}:{:0>2}]{}'.format(tcolor,time_object[3],time_object[4],time_object[5],colors['end']),end='')
	print(prefix, end='')
	if color != None:
		print(colors[color], end='')
	if background != None:
		print(colors['_'+background], end='')
	print(data, end='')
	print(colors['end'], end='')
	print(suffix, end='')
	return 0

if __name__ == '__main__':
	pprint('pprint started. Thanks for using it!', prefix=' ', timestamp=1, timecolor='red')
	pprint('Color example started!', prefix=' ', timestamp=1)
	for color in colors:
		pprint(color, color, prefix=' ', timestamp=1)
	
