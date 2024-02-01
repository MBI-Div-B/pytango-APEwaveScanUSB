# -*- coding: utf-8 -*-
#!/usr/bin/env python

# #############################################################################
#  ATTENTION
# #############################################################################
#
#  This software is for guidance only. It is provided "as is".
#  It only aims at providing coding information to the customer in order for
#  them to save time. As a result no warranties, whether express, implied or
#  statutory, including, but not limited to implied warranties of
#  merchantability and fitness for a particular purpose apply to this software.
#  A·P·E Angewandte Physik und Elektronik GmbH shall not be held liable for any
#  direct, indirect or consequential damages with respect to any claims arising
#  from the content of such sourcecode and/or the use made by customers of the
#  coding information contained herein in connection with their products.
#
#  File Version: 1.1
#
#  Changelog:
#    1.0 - Initial Version
#    1.1 - Python Version check implemented for V>= 3.0 (2015/05/26)
#    1.2 - Code is now compatible with python versions 2.7.x and 3.x
#
# #############################################################################

import socket
import time

class ape_device:
    def __init__(self, host="127.0.0.1", port=51123, name="APEDevice"):
        self.host = host
        self.port = port
        self.name = name
        self.connected = False
        self.dev = None
        self.connect()

    def connect(self):
        if self.connected:
            raise Exception('[Connect] Error. Already Connected')

        elif not isinstance(self.host, str) or not self.host:
            raise Exception('[Connect] Hostname must be passed as string')

        elif not isinstance(self.port, int) or not self.port or not 1 <= self.port <= 65535:
            raise Exception('[Connect] Portnumber must be passed as integer (range 1..65535)')
        else:
            try:
                self.dev = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.dev.connect((self.host, self.port))
                self.connected = True
                time.sleep(1)
                print('Connected to: '+self.host+':'+str(self.port))
                print('--------------------------------------------')

            except:
                import traceback
                traceback.print_exc()
                self.connected = False
                self.dev = None

    def disconnect(self):
        if not self.connected :
            raise Exception('[Disconnect] Not connected')
        else:
            self.dev.close()

    def send(self, command):
        if not self.connected:
            raise Exception('[Send] Error. Not connected')
        else:
            cmd = command.rstrip()+"\r\n"
            self.dev.send(cmd.encode())

    def read_scpi(self):
        if not self.connected:
            raise Exception('[Read_SCPI] Error. Not connected.')
            return bytearray([])
        else:
            if self.receive(1)[0] != ord("#"):
                return bytearray([])
            else:
                header_len = int(self.receive(1).decode())
                if header_len < 0:
                    return bytearray([])
                else:
                    data_len = int(self.receive(header_len).decode())
                    if data_len <= 0:
                        return bytearray([])

                    else:
                        return self.receive(data_len)

    def receive(self, length=-1):
        data_read = length
        answer = bytearray([])
        buffer = bytearray([])
        if not isinstance(length, int):
            raise Exception('[Receive] Data length must be passed as integer')

        if not self.connected:
            raise Exception('[Receive] Error. Not connected')
        else:
            try:
                if length == 0:
                    answer = bytearray([])

                elif length > 0:
                    while data_read > 0:
                        buffer = self.dev.recv(data_read)
                        answer.extend(buffer)
                        data_read -= len(buffer)
                else:
                    while True:
                        buffer = self.dev.recv(1)
                        if buffer[0] != 0:
                            answer.extend(buffer)
                        if buffer[0] == 0x0a:
                            break
            except:
                import traceback
                traceback.print_exc()
                raise Exception('[Receive] Error while reading data')

            return answer

    def query(self, command, block=False):

        answer = bytearray([])
        self.send(command)
        if block == False:
            answer = self.receive().decode().rstrip()
        else:
            answer = self.read_scpi()

        return answer

    def idn(self):
        return self.query("*idn?")

    def stb(self):
        return self.query("*stb?")

    def oper(self):
        return self.query("*oper?")
