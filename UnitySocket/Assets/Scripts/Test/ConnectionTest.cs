using System.Collections;
using System.Collections.Generic;
using PythonConnection;
using Unity.VisualScripting;
using UnityEngine;

public class ConnectionTest : MonoBehaviour
{
    public PythonConnector pythonConnector;

    void Start() { }

    private void OnTimeout()
    {
        Debug.Log("Timeout");
    }
}
