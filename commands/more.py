#!/usr/bin/env python3


import os


meta_data = { "help": ["Shows more data.","Usage: &botcmdmore [amount]"], "aliases": ["more"], "owner": 0 }


def execute(parent, commands, user, host, channel, params):

	with open('commands/more.search', 'r') as more:
		data = more.read()

	with open('commands/more.search', 'w') as more:
		more.write('')