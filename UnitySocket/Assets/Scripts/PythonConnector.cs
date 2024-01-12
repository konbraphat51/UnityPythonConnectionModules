/*
https://github.com/konbraphat51/UnityPythonConnectionClass
Author: Konbraphat51
License: Boost Software License (BSL1.0)
*/

using System;
using System.Collections;
using System.Collections.Generic;
using System.Net.Sockets;
using System.Threading.Tasks;
using UnityEngine;

/// <summary>
/// Connecting to Python
///
/// This will be a client socket to connect to Python server
/// Singleton
/// </summary>
public class PythonConnector : MonoBehaviour
{
    /// <summary>
    /// Returns singleton instance
    /// </summary>
    public static PythonConnector instance
    {
        get
        {
            if (_instance == null)
            {
                _instance = FindObjectOfType<PythonConnector>();

                if (_instance == null)
                {
                    Debug.LogError("PythonConnector not found");
                }
            }
            return _instance;
        }
    }

    /// <summary>
    /// Returns true if currently connected to Python server
    /// </summary>
    public bool connecting { get; private set; }

    /// <summary>
    /// For remember singleton instance
    /// </summary>
    private static PythonConnector _instance;

    [Tooltip("IP Address of Python Server")]
    [SerializeField]
    private string ipAddress = "127.0.0.1";

    [Tooltip("Port of Python Server")]
    [SerializeField]
    private int portPython = 9000;

    [Tooltip("Port of Unity Server")]
    [SerializeField]
    private int portThis = 9001;

    [Tooltip("Buffer size for reading data from Python server. Bytes.")]
    [SerializeField]
    private int bufferSize = 8192;

    [Tooltip("Timeout for receiving data from Python server. Seconds.")]
    [SerializeField]
    private float timeOutReceiving = 10f;

    private TcpClient client;
    private NetworkStream stream;

    /// <summary>
    /// Connect to the Python server
    /// </summary>
    /// <returns>true if succeeded</returns>
    public bool StartConnection()
    {
        try
        {
            //try connecting
            client = new TcpClient(ipAddress, portThis);
            client.Connect(ipAddress, portPython);
            stream = client.GetStream();

            //set timeout
            // to miliseconds
            client.ReceiveTimeout = (int)(timeOutReceiving * 1000f);

            //start listening thread
            Task.Factory.StartNew(OnProcessListening);

            //connection succeeded
            connecting = true;
            return true;
        }
        catch (SocketException)
        {
            //connection failed
            connecting = false;
            return false;
        }
    }

    /// <summary>
    /// Close connection
    /// </summary>
    /// <returns>true if the connection closed successfully. False if not connecting from the beginning</returns>
    public bool StopConnection()
    {
        // if not connecting from the beginning...
        if (!connecting)
        {
            //...show this wasn't closed successfully
            return false;
        }

        //close connection
        stream.Close();
        client.Close();

        connecting = false;

        //show this was closed successfully
        return true;
    }

    /// <summary>
    /// Keep listening to the Python server
    ///
    /// this will be running in a separate thread0
    /// </summary>
    private void OnProcessListening()
    {
        try
        {
            while (true)
            {
                //read data from Python server
                byte[] data = new byte[bufferSize];
                int bytes = stream.Read(data, 0, data.Length);
                string message = System.Text.Encoding.ASCII.GetString(data, 0, bytes);

                //call registered callback
                OnDataReceived(message);
            }
        }
        catch (SocketException)
        {
            StopConnection();
        }
    }

    /// <summary>
    /// Called when received data from Python server.
    ///
    /// This will decode the data and call the registered callback
    /// </summary>
    /// <param name="data"></param>
    private void OnDataReceived(string data) { }
}
