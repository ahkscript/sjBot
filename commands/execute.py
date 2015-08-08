import math
import random
import time
import sys
import re

meta_data = { "help": ["Nothing."], "aliases": ["execute", "exec",'ex', 'e'], "owner": 0 }

def p(data):
    global local_vars
    if '__poutput__' not in local_vars:
        local_vars['__poutput__'] = ''
    local_vars['__poutput__'] = local_vars['__poutput__'] + data + '\n'
    return None

global_vars = {'__builtins__': {'time': time, 'random': random, 'range': range, 'sleep': time.sleep, 'math': math, 'abs': abs, 'all': all, 'any': any, 'ascii': ascii, 'bin': bin, 'bool': bool, 'bytearray': bytearray, 'bytes': bytes, 'callable': callable, 'chr': chr, 'classmethod': classmethod, 'complex': complex, 'dir': dir, 'dict': dict, 'divmod': divmod, 'enumerate': enumerate, 'filter': filter, 'float': float, 'format': format, 'frozenset': frozenset, 'getattr': getattr, 'deleteattr': delattr, 'hasattr': hasattr, 'hash': hash, 'hex': hex, 'id': id, 'int': int, 'isinstance': isinstance, 'issubclass': issubclass, 'iter': iter, 'len': len, 'list': list, 'map': map, 'max': max, 'min': min, 'next': next, 'object': object, 'oct': oct, 'ord': ord, 'pow': pow, 'property': property, 'repr': repr, 'reversed': reversed, 'round': round, 'set': set, 'setattr': setattr, 'slice': slice, 'sorted': sorted, 'staticmethod': staticmethod, 'str': str, 'sum': sum, 'tuple': tuple, 'type': type, 'zip': zip, 'print': p}}

def execute(parent, commands, user, host, channel, params):
    global local_vars
    remove = ['import', 'while', '__loader__']
    replace = ['\r\n', '\r', '\n']
    regremove = ['.*\d\*\*\(']
    local_vars = {'user': user, 'host': host, 'channel': channel, 'params': params}
    
    if any(u in host for u in parent.ownerlist):
        local_vars['sjBot'] = parent
        local_vars['commands'] = commands

    code = '\n'.join(' '.join(params).split('##'))
    safe = ''

    for line in code.split('\n'):
        if any(a in line for a in remove):
            continue
        if line == '':
            continue
        if any(re.search(a, line) is not None for a in regremove):
            line = "print('Could not process that.')"
        safe += line + '\n'

    if safe.split('\n')[1] == '':
        safe = '__output__ = ' + safe.split('\n')[0]
    print( safe )
    try:
        exec(safe, global_vars, local_vars)
    except Exception as Error:
        raise
        return 'An error has occured: ' + str(Error)

    out = ''

    if '__output__' in local_vars:
        out += str(local_vars['__output__']) if local_vars['__output__'] else ''
    if '__poutput__' in local_vars:
        out += ' -- '.join([str(x) for x in local_vars['__poutput__'].split('\n') if x])
    if out != '':
        for rep in replace:
            out = out.replace(rep, '')
        return 'output: ' + str(out)
    return 0
