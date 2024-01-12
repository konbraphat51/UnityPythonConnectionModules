"""
UnityPythonConnectionClass
Writer: Konbraphat51
License: Boost Software License (BSL1.0)
"""

from socket import create_server
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
    :param str finish_code: Code to finish connection
    """
    
    def __init__(self, 
                 port_this:int = 9000,
                 port_unity:int = 9001,
                 ip:str="127.0.0.1", 
                 timeout:float = 3,
                 buffer_size:int = 8192, # 8KB
                 finish_code:str = "!end!"
                 ):
        self.address_this = (ip, port_this)
        self.port_unity = port_unity
        self.timeout = timeout
        self.buffer_size = buffer_size
        self.finish_code = finish_code 
        self.connecting = False
        self.socket = None
    
    def start_listening(self, overwriting: bool = False) -> None:
        """
        Start listening to Unity
        
        :param bool overwriting: If True, overwrite the current connection if already connecting
        :rtype: None
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
            
        # start listening thread
        self.thread = threading.Thread(target=self._run_connection)
            
    def stop_connection(self) -> bool:
        """
        Close connection
        
        :param bool error_when_not_connecting: If True, raise error when not connecting
        :return: True if connection is closed successfully, False if not connecting from the beginning
        :rtype: bool
        """
        
        # if not connecting...
        if not self.connecting:
            #...show this wasn't connecting from the beginning
            return False
        
        #stop connection
        self.socket.close()
        
        #change flag
        self.connecting = False

        # closed successfully
        return True
            
    def _run_connection(self):
        """
        Run connection
        
        This function is called when the connection is established
        """
        # start connection
        self.connecting = True
        
        #establish
        self._wait_connection_established()
        
        # loop for receiving data
        while True:
            # receive data
            data = self.socket.recv(self.buffer_size).decode()
            
            # if finish code received...
            if data == self.finish_code:
                # ...stop connection
                self.stop_connection()
            
            # do something with data
            self._report_received_data(data)
        
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