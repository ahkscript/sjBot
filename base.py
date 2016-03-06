#!/usr/bin/env python3


import socket
import time
import threads


class Connection():

    def __init__(self, network, port=6667, password=None):
        """__init__
        creates and or sets some default variables

        params:

        network:    str:    The network for the bot to join.
        port:       int:    The port for the bot to join on.
                            Default 6667
        password:   str:    The password for the server.

        NOTE:

        password is NOT the password for NickServ or other
        identification bots the server may have.
        """
        self.network = network
        self.port = port
        self.socket = None
        self.nickname = None
        self.user = None
        self.host = None
        self.realname = None
        self.handler = handler
        self.password = None
        self.rate_limit = [4, 3]
        self.previous_sendtime = None
        self.previous_sent = []
        self.running = True
        self.use_history = False
        self.history = []
        self.display_func = print

    def __enter__(self):
        return self

    def __exit__(self, ctx_type, ctx_value, ctx_traceback):
        self.close_connection()
        return None
    
    def display(self, text, padding=True):
        """display
        A simple print() wrapper that prepends some data such as 
        network and nickname.

        params:

        text:   str:    The text to send to print.
        """
        if padding:
            self.display_func('{} - {} - {}'.format(self.network,
                              self.nickname, text))
        else:
            self.display_func('{}'.format(text))
        return None

    def send(self, data):
        """send
        Sends some data to the connected server.
        The data being sent is also displayed so you know what is
        going on.

        There are also some error checks and connection checks
        to make sure the data is sent. If not, it attempts to
        reconnect.

        This also has a built in rate limit, based off the
        self.rate_limit variable. self.rate_limit = [a, t]
        a = the amount it needs before it limits.
        t = the time to sleep before sending more data.

        params:

        data:   str:    The data to send to the server.

        NOTE:

        This function automatically appends \r\n to the end
        of the data. So there is no need to send it.

        This function also automatically converts to bytes
        so all you need to do is send something like

        .send("PRIVMSG #channel :Hello")

        and it will work
        """
        if (self.previous_sendtime is not None and 
                time.time() - self.previous_sendtime <
                self.rate_limit[1] and
                len(self.previous_sent) > self.rate_limit[0]):
            time.sleep(self.rate_limit[1])
            self.previous_sent = []

        self.previous_sendtime = time.time()
        self.previous_sent.append(data)

        if self.socket is None:
            self.display('[SOCKET-ERROR] Socket is empty.')
            return 1
        try:
            sent = self.socket.send('{}\r\n'.format(data).encode('utf-8'))
        except Exception:
            sent = 0
        if sent == 0:
            self.display('[SOCKET-OUT-ERROR] Did not / Could not send.')
            connected = self.reconnect()
            if not connected:
                return 1
        else:
            self.display('[SOCKET-OUT] {}'.format(data))
        return None

    def set_ident(self, nickname, user='sjBot',
                  host='Uptone-Software',
                  realname='Uptone-software/Bot'):
        """set_ident
        Sets the identity of the bot. You MUST call this function 
        before you attempt to .connect()

        params:

        nickname:   str:    The nickname of the bot.
        user:       str:    The user of the bot.
        host:       str:    The host of the bot.
        realname:   str:    The bots real name, this shows up in a 
                            /whois.
        """
        self.nickname = nickname
        self.user = user
        self.host = host
        self.realname = realname
        return None

    def set_handler(self, handler, functions):
        """set_handler
        Sets the function / method that will receive the incoming data.
        The data is first processed by this class, then passed to the 
        handler.

        params:

        handler:    function:       The function or method that will
                                    receive incoming data.
        functions:  dict:           A list of functions that the handler
                                    will be able to access.

        NOTE:

        ERROR's and PING's will not be sent to this handler.
        They will be automatically passed to a method of this class.
        """
        self.handler = handler
        self.handler_functions = functions
        return None

    def identify(self):
        """identify
        Sends the bots identity to the server.
        If there is a password set he will send that first.
        """
        self.display('[IDENT] Sending identification information.')
        if self.password is not None:
            self.send('PASS {}'.format(self.password))
        self.send('NICK {}'.format(self.nickname))
        self.send('USER {} {} {} :{}'.format(self.nickname, self.user, 
                  self.host, self.realname))
        return None

    def connect(self, attempts=10, delay=5):
        """connect
        Attempts to connect to the server.
        This will return True if it connects and False if it doesn't.

        params:

        attempts:   int:    The number of attempts to make, it will 
                            stop if it can connect.
        delay:      int:    The delay between each connection attempt.
        """
        # Check if all of the needed info has been set.
        if (self.nickname is None or self.user is None or self.host is None or
                self.realname is None):
            self.display('[IDENT] You need to set the ident before '
                         'connecting.')
            return 1
        
        self.display('[SOCKET] Creating the socket connection.')
        
        self.socket = socket.socket()

        # Attempt to connect to the server. It will try the number
        # in the attempts param before giving up.

        for attempt in range(attempts):
            try:
                self.display('[SOCKET] Connecting to {} - {}'.format(
                             self.network, self.port))
                self.socket.connect((self.network, self.port))
            except Exception as error:
                sleep_time = delay * (attempt+1)
                self.display('[SOCKET] Connection {} failed. {}'.format(
                             attempt+1, error))
                self.display('[SOCKET] Waiting for {} seconds before '
                             'retrying.'.format(sleep_time))
                time.sleep(sleep_time)
                continue
            else:
                self.display('[SOCKET] Connected!')
                return True
        return False

    def reconnect(self, delay=30):
        """reconnect
        Attempts to reconnect, this is basically a padded wrapper for 
        the connect method.
        
        There are no params passed to connect, so it will try to 
        connect with the default params.

        This returns True if it could reconnect, False otherwise.

        params:

        delay:      int:    The delay before it starts the connect
                            loop.
        """
        self.display('[SOCKET] Attempting to reconnect in {} seconds'.format(
                     delay))
        time.sleep(delay)
        connected = self.connect()
        if not connected:
            self.display('[SOCKET] Could not reconnect.')
        else:
            self.identify()
        return connected

    @threads.asthread()
    def receive_loop(self):
        """receive_loop
        This threaded loop handles all the incoming data.
        It will check the data and then either pass it to the handler 
        function, handle_error method or pong method.

        returns:

        1       If the .handler variable has not been set.
        2       if the bot loses connection and cannot reconnect.
        """
        if self.handler is None:
            self.display('[ERROR] You need to set a .handler function before '
                         'you can use the receive_loop method.')
            return 1
        previous = ''
        while self.running:
            try:
                recv = self.socket.recv(1024).decode('utf-8')
            except UnicodeDecodeError as e:
                self.display('[SOCKET-IN-ERROR] {}'.format(e))
            except ConnectionResetError:
                connected = self.reconnect()
                if not connected:
                    return 2
            
            if recv.endswith('\r\n'):
                self.handler(self, previous + recv, self.handler_functions)
                previous = ''
            else:
                previous += recv
        return None

    def join(self, channel):
        """join
        Makes the bot join a channel.

        params:

        channel:    str:    The channel to join.
        """
        self.send('JOIN {}'.format(channel))
        return None

    def privmsg(self, channel, message):
        """privmsg
        Sends a message to a person/channel.

        params:

        channel:    str:    The channel/person to send to.
        message:    str:    The message to send.
        """
        self.send('PRIVMSG {} :{}'.format(channel, message))
        return None

    def set_nickname(self, nickname):
        """set_nickname
        Sets the nickname of the bot. This changes the .nickname var
        and sends NICK to the server

        params:

        nickname:       str:        The new nickname of the bot.
        """
        self.nickname = nickname
        self.send('NICK {}'.format(nickname))
        return None

    def close_connection(self):
        """close_connection
        Closes the connection to the socket and clears the variable.
        """
        self.send('QUIT :Bye!')
        self.socket.close()
        self.running = False
        self.socket = None
        return None


def handler(connection, data, functions):
    """handler

    A default handler function that the user can specify for the data
    handler. Either this or make thier own.

    params:

    connection:     Connection:     The Connection instance that
                                    is being handled.
    data:           str:            The IRC data that is being passed
                                    in.
    functions:      dict:           A dictionary of functions that will
                                    be used to check for event 
                                    functions.
    """
    for line in data.split('\r\n'):
        if line == '':
            continue
        connection.display('[SOCKET-IN] {}'.format(line))
        spaced = line.split(' ')
        first_check = 'r_{}'.format(spaced[0])
        second_check = 'r_{}'.format(spaced[1])
        if first_check in functions:
            functions[first_check](connection, *spaced[1:])
        elif second_check in functions:
            functions[second_check](connection, *[spaced[0]] + spaced[2:])
        if 'r_ALL' in functions:
            functions['r_ALL'](connection, *spaced)
    return None