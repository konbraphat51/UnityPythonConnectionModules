"""
UnityPythonConnectionClass
Writer: Konbraphat51
License: Boost Software License (BSL1.0)
"""

from socket import socket
import threading

class UnityConnector:
    """
    Connect your python script to Unity
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
        
    
    def start_connection(self, first = True):
        """
        Start connection to Unity
        
        :param bool first: If this (Python) started connection earlier than Unity, set this to True.
            If True, this will wait for Unity connection
        """
        
        