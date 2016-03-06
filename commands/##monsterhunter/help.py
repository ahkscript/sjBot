#!/usr/bin/env python3


import inspect


owner = False
aliases = ['helpmeplz']


def help(con, sjBot, commands, trigger, host, channel, command=None):
    """Shows information about commands."""
    if command is None:
        output = []
        output.append('Here is a list of commands: {}.'.format(', '.join(
                    sorted(commands))))
        output.append('Use \x1F{}help command\x1F for more '
                      'info'.format(trigger))
    else:
        if command in commands:
            func = getattr(commands[command], command)
            docs = inspect.getdoc(func)
            if docs is None:
                docs = 'There are no docs for this commands.'
            else:
                docs = docs.replace('\n', ' ')
            output = [docs]
            params = inspect.signature(func).parameters
            param_info = 'Usage: {}{}'.format(trigger, command)
            for i, p in enumerate(params):
                if i < 6:
                    continue

                if (params[p].default == params[p].empty and 
                        params[p].kind != params[p].VAR_POSITIONAL):
                    param_info += ' \x02<{}>\x02'.format(p)
                elif params[p].kind == params[p].VAR_POSITIONAL:
                    param_info += ' \x1D*{}\x1D'.format(p)
                else:
                    param_info += ' \x1F[{}]\x1F'.format(p)

            output.append(param_info)
    user = host.split('!')[0][1:]
    for line in output:
        con.privmsg(user, line)
    return None