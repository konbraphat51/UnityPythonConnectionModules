"""
UnityPythonConnectionClass
Writer: Konbraphat51
License: Boost Software License (BSL1.0)
"""

from socket import socket, AF_INET, SOCK_STREAM, create_server
import threading

class UnityConnector:
    """
    Connect your python script to Unity
    
    Python listen (wait) for Unity to comming to connect.
    
    :param int port_this: Port this (Python) allocated
    :param int port_unity: Port Unity allocated
    :param str ip: IP to connect to
    :param float timeout: Timeout for connection
    :param int buffer_size: Buffer size for receiving data
    """
    
    def __init__(self, 
                 port_this:int = 9000,
                 port_unity:int = 9001,
                 ip:str="127.0.0.1", 
                 timeout:float = 3,
                 buffer_size:int = 8192 # 8KB
                 ):
        self.address_this = (ip, port_this)
        self.port_unity = port_unity
        self.timeout = timeout
        self.buffer_size = buffer_size
        self.connecting = False
        self.socket = None
    
    def start_listening(self, overwriting: bool = False):
        """
        Start listening to Unity
        
        :param bool overwriting: If True, overwrite the current connection if already connecting
        """
        
        # if this is already connecting...
        if self.connecting:
            # ...if should overwrite the current connection...
            if overwriting:
                # ...close the current connection
                self.socket.close()
            # ...if should not overwrite the current connection...
            else:
                raise Exception("Already connecting")
            
    def _listen_connection(self):
        
    def _wait_connection_established(self):
        """
        Wait until Unity connect to this
        
        Make a server and wait until Unity connect to this
        """
        
        #make server
        self.server = create_server(self.address_this)
        
        #wait connected with port_unity
        #loop for the specified port detected (ignore others)
        while True:
            self.socket, self.address_unity = self.server.accept()
            if self.address_unity[1] == self.port_unity:
                break