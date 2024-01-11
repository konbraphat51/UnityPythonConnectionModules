"""
UnityPythonConnectionClass
Writer: Konbraphat51
License: Boost Software License (BSL1.0)
"""

from socket import socket, AF_INET, SOCK_STREAM
import threading

class UnityConnector:
    """
    Connect your python script to Unity
    
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
        self.address_unity = (ip, port_unity)
        self.timeout = timeout
        self.buffer_size = buffer_size
        self.connecting = False
        self.socket = None
    
    def start_connection(self, first: bool = True, overwriting: bool = False):
        """
        Start connection to Unity
        
        :param bool|None first: If this (Python) started connection earlier than Unity, set this to True.
            If True, this will wait for Unity connection,
            if False, this will connect to Unity which is waiting
        :param bool overwriting: If True, overwrite the current connection if already connecting
        """
        
        # if Unity is waiting for connection...
        if not first:
            # ...connect to Unity
            self._create_connection(overwriting)
        
    def _create_connection(self, overwriting: bool = True) -> socket:
        """
        Connect to the waiting Unity
        
        :param bool overwriting: If True, overwrite the current connection
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
            
        # connect to Unity
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind(self.address_this) # set the sender address (this)
        self.socket.connect(self.address_unity) # destination address (Unity)
    
    def _start_server(self):
        """
        Start socket server
        """
        
        self.thread = threading.Thread(target=self._server_thread)
        self.thread.start()