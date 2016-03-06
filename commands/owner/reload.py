#!/usr/bin/env 


def reload(con, sjBot, commands, trigger, host, channel):
    """Reloads the commands and plugins."""
    sjBot['load_commands']()
    sjBot['load_settings']()
    sjBot['load_plugins']()
    return 'Reloaded commands and plugins!'