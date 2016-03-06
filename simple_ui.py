#!/usr/bin/env python3


import curses, curses.textpad, curses.ascii
import os
import threads


class Interface():

    text = []
    network = 'None'
    channel = 'None'

    def __init__(self, message_handler):
        rows, columns = os.popen('stty size', 'r').read().split()
        self.rows, self.columns = (rows, columns)
        self.message_handler = message_handler
        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.use_default_colors()

        for index in range(curses.COLORS):
            curses.init_pair(index + 1, index, -1)

        self.screen.keypad(1)
        self.screen.clear()
        self.screen.refresh()
        self.screen.addstr(0, 0, 'sjBot terminal interface!'.center(
                          int(columns)), curses.color_pair(8) | 
                          curses.A_REVERSE)
        self.screen.refresh()
        self.editarea = curses.newwin(0, int(columns)-1, int(rows)-1, 1)
        self.textbox = curses.textpad.Textbox(self.editarea)
        self.textarea = curses.newwin(int(rows)-4, int(columns)-1, 1, 1)
        self.channelarea = curses.newwin(1, int(columns)-1, int(rows)-3, 1)

    def display(self, text):
        self.text.append(text)
        self.textarea.clear()
        for index, text in enumerate(self.text[-(int(self.rows)-7):]):
            ascii = ''.join([curses.ascii.ascii(x) for x in text])
            self.textarea.addstr(index+1, 1, ascii)
            self.textarea.refresh()
        return None

    def refresh_all(self):
        self.screen.clear()
        self.screen.refresh()
        self.channelarea.clear()
        self.channelarea.addstr('[{}/{}]'.format(self.network, self.channel))
        self.channelarea.refresh()
        return None
    
    @threads.asthread()
    def handle_input(self):
        while True:
            self.channelarea.clear()
            self.channelarea.addstr('[{}/{}]'.format(self.network, 
                                    self.channel).center(int(self.columns)-2),
                                    curses.color_pair(8) | curses.A_REVERSE)
            self.channelarea.refresh()
            message = self.textbox.edit()
            self.editarea.clear()
            self.editarea.refresh()
            self.message_handler(self, message)
        return None



if __name__ == '__main__':
    ui = Interface()