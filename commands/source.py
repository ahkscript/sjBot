#!/usr/bin/env python3


meta_data = { "help": ["Displays the source code link of the bot"], "aliases": ["source", "sc", "sourcecode"], "owner": 0 }
url = 'https://github.com/ahkscript/sjBot'


def execute(*junk):
	return ['My source can be found at ' + url]