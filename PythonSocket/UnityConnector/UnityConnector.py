"""
UnityPythonConnectionClass
Writer: Konbraphat51
License: Boost Software License (BSL1.0)
"""

from socket import create_server, socket
import threading
import json

class UnityConnector:
    """
    Connect your python script to Unity
    
    Python listen (wait) for Unity to comming to connect.
    
    If structure/rule of data for communication is changed, you can override encode() and decode() function.
    
    :param int port_this: Port this (Python) allocated
    :param int port_unity: Port Unity allocated
    :param str ip: IP to connect to
    :param float timeout_receiving: How many seconds to wait for receive next data from Unity
    :param float timeout_establishing: How many seconds to wait for establish connection with Unity
    :param callable on_timeout: Function to call when timeout
    :param int buffer_size: Buffer size for receiving data
    :param str finish_code: Code to finish connection
    """
    
    def __init__(self,
                 port_this:int = 9000,
                 port_unity:int = 9001,
                 ip:str="127.0.0.1",
                 timeout_receiving:float = 120,
                 timeout_establishing:float = 300,
                 on_timeout:callable = lambda: None, 
                 buffer_size:int = 8192, # 8KB
                 finish_code:str = "!end!"
                 ) -> None:
        self.address_this = (ip, port_this)
        self.port_unity = port_unity
        self.timeout_receiving = timeout_receiving
        self.timeout_establishing = timeout_establishing
        self.on_timeout = on_timeout
        self.buffer_size = buffer_size
        self.finish_code = finish_code 
        self.connecting = False
        self.socket = None
    
    def start_listening(self, on_data_received: callable, overwriting: bool = False) -> None:
        """
        Start listening to Unity
        
        :param callable on_data_received: Function to call when data is received
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
            
        # remember callback
        self.on_data_received = on_data_received   
        
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
    
    def send(self, data:dict) -> bool:
        """
        Send data to Unity
        
        :param dict data: Data to send
        :return: True if data is sent successfully, False if not connecting
        :rtype: bool
        """
        
        # if not connecting...
        if not self.connecting:
            #...show this wasn't connecting from the beginning
            return False
        
        #encode data
        data_encoded = self.encode(data)
        
        #send data
        self.socket.send(data_encoded.encode())
        
        # sent successfully
        return True
    
    def encode(self, data:dict) -> str:
        """
        Encode data to send to Unity
        
        The default encoding is to JSON.
        If you want to change the encoding, override this function.
        
        :param dict data: Data to encode
        :return: Encoded data
        :rtype: str
        """
        
        return json.dumps(data)
            
    def decode(self, data:str) -> dict:
        """
        Decode data received from Unity
        
        The default decoding is to JSON.
        If you want to change the decoding, override this function.
        
        :param str data: Data to decode
        :return: Decoded data
        :rtype: dict
        """
        
        return json.loads(data)
            
    def _run_connection(self) -> None:
        """
        Run connection
        
        This function is called when the connection is established
        """
        
        #establish
        establish_succeeded = self._wait_connection_established()
        
        # if connection failed...
        if not establish_succeeded:
            # ...quit
            return
        
        # loop for receiving data
        while True:
            try:
                # set timeout for receiving
                self.socket.settimeout(self.timeout_receiving)
                
                # receive data
                data = self.socket.recv(self.buffer_size).decode()
                
                # if finish code received...
                if data == self.finish_code:
                    # ...stop connection
                    self.stop_connection()
                    break
                
                # do something with data
                self._report_received_data(data)
                
            # if timeout...
            except socket.timeout:
                # ...quit connection
                
                # call timeout callback
                self.on_timeout()
                
                # ...stop connection
                self.stop_connection()
                break
        
    def _wait_connection_established(self) -> bool:
        """
        Wait until Unity connect to this
        
        Make a server and wait until Unity connect to this
        
        :return: True if connection is established successfully, False if timeout
        :rtype: bool
        """
        
        #make server
        self.server = create_server(self.address_this)
        
        #set timeout for establishing
        self.server.settimeout(self.timeout_establishing)
        
        
        try:
            #wait connected with port_unity
            #loop for the specified port detected (ignore others)
            while True:
                socket, address = self.server.accept()
                # if port_unity detected...
                if address[1] == self.port_unity:
                    # ...start connection
                    self.connecting = True
                    
                    # remember socket
                    self.socket = socket
                    self.address_unity = address
                    
                    # connection established successfully
                    return True
                
                # if dirrerent port detected...
                else:
                    # ...not dealing with this
                    socket.close()
                    
        # if timeout...
        except socket.timeout:
            # ...quit connection
            
            # call timeout callback
            self.on_timeout()
            
            # connection failed
            return False
            
    def _report_received_data(self, data:str) -> None:
        """
        Report received data
        
        :param str data: Data received
        :rtype: None
        """
        
        #decode data
        data = self.decode(data)
        
        #report
        self.on_data_received(data)