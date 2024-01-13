"""
UnityPythonConnectionClass
Writer: Konbraphat51
License: Boost Software License (BSL1.0)
"""

from __future__ import annotations
from socket import AF_INET, SOCK_STREAM, timeout
from socket import socket as Socket
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
    :param callable on_stopped: Function to call when connection is stopped by Unity
    :param int buffer_size: Buffer size for receiving data
    :param str finish_code: Code to finish connection
    """

    def __init__(
        self,
        port_this: int = 50001,
        port_unity: int = 50002,
        ip: str = "127.0.0.1",
        timeout_receiving: float = 120,
        timeout_establishing: float = 300,
        on_timeout: callable = lambda: None,
        on_stopped: callable = lambda: None,
        buffer_size: int = 8192,  # 8KB
        finish_code: str = "end!",
    ) -> None:
        self.address_this = (ip, port_this)
        self.port_unity = port_unity
        self.timeout_receiving = timeout_receiving
        self.timeout_establishing = timeout_establishing
        self.on_timeout = on_timeout
        self.on_stopped = on_stopped
        self.buffer_size = buffer_size
        self.finish_code = finish_code
        self.connecting = False
        self.socket = None

    def start_listening(
        self, on_data_received: callable, overwriting: bool = False
    ) -> bool:
        """
        Start listening to Unity

        :param callable on_data_received: Function to call when data is received
            Param data_type(string), data(dict) will be passed to this function
        :param bool overwriting: If True, overwrite the current connection if already connecting
        :return: True if connection is established successfully, False if timeout
        :rtype: bool
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

        # establish connection
        establish_succeeded = self._wait_connection_established()

        # if connection failed...
        if not establish_succeeded:
            # ...failed
            return False

        # start listening thread
        self.thread = threading.Thread(target=self._run_connection)

        # success
        return True

    def stop_connection(self) -> bool:
        """
        Close connection

        :return: True if connection is closed successfully, False if not connecting from the beginning
        :rtype: bool
        """

        # if not connecting...
        if not self.connecting:
            # ...show this wasn't connecting from the beginning
            return False

        # send stop code
        self._send_str(self.finish_code)

        # stop connection
        self.socket.close()

        # change flag
        self.connecting = False

        # closed successfully
        return True

    def send(self, data_type: str, data: dict) -> bool:
        """
        Send data to Unity

        This will send "<data_type>!<data json>" to Unity, if encode() not overrided.

        :param str data_type: Type of data
        :param dict data: Data to send
        :return: True if data is sent successfully, False if not connecting
        :rtype: bool
        """

        # encode data
        data_encoded = self.encode(data_type, data)

        # send data
        return self._send_str(data_encoded)

    def encode(self, data_type: str, data: dict) -> str:
        """
        Encode data to send to Unity

        The default encoding is to JSON.
        If you want to change the encoding, override this function.

        :param dict data: Data to encode
        :return: Encoded data
        :rtype: str
        """

        data_json = json.dumps(data)

        return f"{data_type}!{data_json}"

    def decode(self, data: str) -> tuple[str, dict]:
        """
        Decode data received from Unity

        The default decoding is to data_type + JSON.
        If you want to change the decoding, override this function.

        :param str data: Data to decode
        :return: (data_type, data)
        :rtype: tuple[str, dict]
        """

        data_type, json_raw = data.split("!", 1)

        json_data = json.loads(json_raw)

        return (data_type, json_data)

    def _send_str(self, data_str: str) -> bool:
        """
        Send string to Unity

        :param str data: string data to send
        :return: True if data is sent successfully, False if not connecting
        :rtype: bool
        """

        # if not connecting...
        if not self.connecting:
            # ...show this wasn't connecting from the beginning
            return False

        # send data
        self.socket.send(data_str.encode())

        # sent successfully
        return True

    def _run_connection(self) -> None:
        """
        Run connection

        This function is called when the connection is established
        """

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

                    # call stopped callback
                    self.on_stopped()

                    break

                # do something with data
                self._report_received_data(data)

            # if timeout...
            except timeout:
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

        # make server
        self.server = Socket(AF_INET, SOCK_STREAM)
        self.server.bind(self.address_this)
        self.server.listen()

        # set timeout for establishing
        self.server.settimeout(self.timeout_establishing)

        try:
            # wait connected with port_unity
            # loop for the specified port detected (ignore others)
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
        except timeout:
            # ...quit connection

            # call timeout callback
            self.on_timeout()

            # connection failed
            return False

    def _report_received_data(self, data: str) -> None:
        """
        Report received data

        :param str data: Data received
        :rtype: None
        """

        # decode data
        data_type, data = self.decode(data)

        # report
        self.on_data_received(data_type, data)
