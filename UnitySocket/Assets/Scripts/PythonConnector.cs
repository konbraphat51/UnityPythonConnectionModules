/*
https://github.com/konbraphat51/UnityPythonConnectionClass
Author: Konbraphat51
License: Boost Software License (BSL1.0)
*/

using System.Collections;
using System.Collections.Generic;
using System.Net.Sockets;
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

    public bool StartConnection()
    {
        return true;
    }
}
