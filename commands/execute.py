import math
import random
import time
import sys

meta_data = { "help": ["Nothing."], "aliases": ["execute", "exec",'ex', 'e'], "owner": 0 }

def p(data):
    global local_vars
    local_vars['__output__'] = data
    return None

global_vars = {'__builtins__': {'time': time, 'random': random, 'range': range, 'sleep': time.sleep, 'math': math, 'abs': abs, 'all': all, 'any': any, 'ascii': ascii, 'bin': bin, 'bool': bool, 'bytearray': bytearray, 'bytes': bytes, 'callable': callable, 'chr': chr, 'classmethod': classmethod, 'complex': complex, 'dir': dir, 'dict': dict, 'divmod': divmod, 'enumerate': enumerate, 'filter': filter, 'float': float, 'format': format, 'frozenset': frozenset, 'getattr': getattr, 'deleteattr': delattr, 'hasattr': hasattr, 'hash': hash, 'hex': hex, 'id': id, 'int': int, 'isinstance': isinstance, 'issubclass': issubclass, 'iter': iter, 'len': len, 'list': list, 'map': map, 'max': max, 'min': min, 'next': next, 'object': object, 'oct': oct, 'ord': ord, 'pow': pow, 'property': property, 'repr': repr, 'reversed': reversed, 'round': round, 'set': set, 'setattr': setattr, 'slice': slice, 'sorted': sorted, 'staticmethod': staticmethod, 'str': str, 'sum': sum, 'tuple': tuple, 'type': type, 'zip': zip, 'print': p}}

def execute(parent, commands, user, host, channel, params):
    global local_vars
    remove = ['import', 'while']
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
        safe = safe + '\n' + line
    try:
        exec(safe, global_vars, local_vars)
    except Exception as Error:
        return 'An error has occured: ' + str(Error)

    if '__output__' in local_vars:
        return ['output: ' + str(local_vars['__output__'])]
    return 0
