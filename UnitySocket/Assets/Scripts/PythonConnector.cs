/*
https://github.com/konbraphat51/UnityPythonConnectionClass
Author: Konbraphat51
License: Boost Software License (BSL1.0)
*/

using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;
using UnityEngine;
using UnityEngine.Events;

namespace PythonConnection
{
    /// <summary>
    /// Connecting to Python
    ///
    /// This will be a client socket to connect to Python server
    /// Singleton
    /// </summary>
    [RequireComponent(typeof(DataDecoder))]
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
        private int portPython = 50001;

        [Tooltip("Port of Unity Server")]
        [SerializeField]
        private int portThis = 50002;

        [Tooltip("Buffer size for reading data from Python server. Bytes.")]
        [SerializeField]
        private int bufferSize = 8192;

        [Tooltip("Timeout for receiving data from Python server. Seconds.")]
        [SerializeField]
        private float timeOutReceiving = 10f;

        [Tooltip("Event called when timeout")]
        [SerializeField]
        private UnityEvent onTimeOut = new UnityEvent();

        [Tooltip("Event called when stopped connection by Python server")]
        [SerializeField]
        private UnityEvent onStopped = new UnityEvent();

        [Tooltip("If get this string, will finish connection")]
        [SerializeField]
        private string finishString = "end!";

        private TcpClient client;
        private NetworkStream stream;

        protected virtual void Update()
        {
            if (connecting)
            {
                ReceiveData();
            }
        }

        /// <summary>
        /// Connect to the Python server
        /// </summary>
        /// <returns>true if succeeded</returns>
        public bool StartConnection()
        {
            try
            {
                //prepare TCP client
                IPEndPoint endPoint = new IPEndPoint(IPAddress.Parse(ipAddress), portThis);
                client = new TcpClient(endPoint);

                //try connecting to Python
                client.Connect(IPAddress.Parse(ipAddress), portPython);
                stream = client.GetStream();

                //connection succeeded
                connecting = true;
                return true;
            }
            catch (SocketException e)
            {
                Debug.Log(e);

                //connection failed
                connecting = false;

                onTimeOut.Invoke();

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

            //send finish string
            Send(finishString);

            //close connection
            stream.Close();
            client.Close();

            connecting = false;

            //show this was closed successfully
            return true;
        }

        /// <summary>
        /// Send data to Python server by JSON
        ///
        /// This will send "<data_type>!<data json>" to Unity, if Encode() not overrided.
        /// </summary>
        /// <typeparam name="T">Serializable class</typeparam>
        /// <param name="dataType"> name of the data type. This will be used to decode the data in Python</param>
        /// <param name="data">Serializable class instance. This will be converted to JSON</param>
        /// <returns>if the data was sent successfully. False if not connecting from the beginning</returns>
        public virtual bool Send<T>(string dataType, T data)
        {
            //to JSON string
            return Send(Encode(dataType, data));
        }

        /// <summary>
        /// Send data to Python server by string
        /// </summary>
        /// <param name="data">string data</param>
        /// <returns>if the data was sent successfully. False if not connecting from the beginning</returns>
        public virtual bool Send(string data)
        {
            //if not connecting from the beginning...
            if (!connecting)
            {
                //...show this wasn't sent successfully
                return false;
            }

            //encode data
            byte[] bytes = Encoding.UTF8.GetBytes(data);

            //send data
            stream.Write(bytes, 0, bytes.Length);

            //show this was sent successfully
            return true;
        }

        /// <summary>
        /// Add callback when received data from Python server
        /// </summary>
        /// <param name="dataType">type of dataclass</param>
        /// <param name="callback">callback called</param>
        public void RegisterAction(Type dataType, UnityAction<DataClass> callback)
        {
            GetComponent<DataDecoder>().RegisterAction(dataType, callback);
        }

        /// <summary>
        /// Remove callback when received data from Python server
        /// </summary>
        /// <param name="dataType">type of dataclass</param>
        /// <param name="callback">callback called</param>
        public void RemoveAction(Type dataType, UnityAction<DataClass> callback)
        {
            GetComponent<DataDecoder>().RemoveAction(dataType, callback);
        }

        /// <summary>
        /// Add callback when timeout
        /// </summary>
        /// <param name="callback">this will be called when timeout</param>
        public void RegisterTimeoutAction(UnityAction callback)
        {
            onTimeOut.AddListener(callback);
        }

        /// <summary>
        /// Remove callback when timeout
        /// </summary>
        /// <param name="callback">this will be called when timeout</param>
        public void RemoveTimeoutAction(UnityAction callback)
        {
            onTimeOut.RemoveListener(callback);
        }

        /// <summary>
        /// Add callback when stopped by Python server
        /// </summary>
        /// <param name="callback">this will be called when stopped by Python server</param>
        public void RegisterStoppedAction(UnityAction callback)
        {
            onStopped.AddListener(callback);
        }

        /// <summary>
        /// Remove callback when stopped by Python server
        /// </summary>
        /// <param name="callback">this will be called when stopped by Python server</param>
        public void RemoveStoppedAction(UnityAction callback)
        {
            onStopped.RemoveListener(callback);
        }

        /// <summary>
        /// Data received from Python server
        /// </summary>
        protected struct Message
        {
            public string dataType;
            public string dataJson;
        }

        /// <summary>
        /// Called when received data from Python server.
        ///
        /// This will decode the data and call the registered callback
        /// </summary>
        /// <param name="data"></param>
        protected virtual void OnDataReceived(string data)
        {
            //separate data_type and data JSON
            Message[] messages = Separate(data);

            foreach (Message message in messages)
            {
                //to Decoder
                GetComponent<DataDecoder>()
                    .DecodeAndReport(message.dataType, message.dataJson);
            }
        }

        /// <summary>
        /// Change data to JSON
        /// </summary>
        /// <typeparam name="T">Serializable class</typeparam>
        /// <param name="data">Serializable class instance</param>
        /// <returns>JSON string</returns>
        protected virtual string Encode<T>(string dataType, T data)
        {
            return dataType + "!" + JsonUtility.ToJson(data);
        }

        /// <summary>
        /// Decode received data to Serializable class
        /// </summary>
        protected virtual Message[] Separate(string data)
        {
            //seperate by start/end tag
            List<string> contents = new List<string>();
            const string startTag = "<s>";
            const string endTag = "<e>";
            while (true)
            {
                int startIndex = data.IndexOf(startTag);
                int endIndex = data.IndexOf(endTag);

                if (startIndex == -1 || endIndex == -1)
                {
                    break;
                }

                //seperate data_type and data JSON
                int length = endIndex - startIndex - startTag.Length;
                string content = data.Substring(startIndex + startTag.Length, length);
                contents.Add(content);

                // if got to the end...
                if (endIndex == data.Length - endTag.Length)
                {
                    //...stop
                    break;
                }
                else
                {
                    //... to the next iteration
                    data = data.Substring(endIndex + endTag.Length);
                }
            }

            //decode each content
            Message[] messages = new Message[contents.Count];
            for (int cnt = 0; cnt < contents.Count; cnt++)
            {
                Message message = new Message();

                //devide to data_type and data JSON
                string[] splited = contents[cnt].Split('!', 2);
                message.dataType = splited[0];
                message.dataJson = splited[1];

                messages[cnt] = message;
            }

            return messages;
        }

        /// <summary>
        /// Keep listening to the Python server
        /// </summary>
        private void ReceiveData()
        {
            try
            {
                if (stream.DataAvailable)
                {
                    //read all data from Python server
                    byte[] data = new byte[bufferSize];
                    string message = "";
                    using (MemoryStream ms = new MemoryStream())
                    {
                        while (stream.DataAvailable)
                        {
                            int readBytes = stream.Read(data, 0, data.Length);
                            ms.Write(data, 0, readBytes);
                        }

                        message = Encoding.UTF8.GetString(ms.ToArray());
                    }

                    //handle stop code
                    if (message == finishString)
                    {
                        //stop connection
                        StopConnection();

                        //action when stopped by Python server
                        onStopped.Invoke();

                        //stop listening
                        return;
                    }

                    //call registered callback
                    OnDataReceived(message);
                }
            }
            catch (SocketException)
            {
                //stop connection
                StopConnection();

                //action when timeout
                onTimeOut.Invoke();
            }
        }
    }
}
