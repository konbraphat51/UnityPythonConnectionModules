using System;
using System.Collections;
using System.Collections.Generic;
using PythonConnection;
using Unity.VisualScripting;
using UnityEngine;

public class ConnectionTest : MonoBehaviour
{
    [Serializable]
    private class SendingData
    {
        public SendingData(int testValue0, List<float> testValue1)
        {
            this.testValue0 = testValue0;
            this.testValue1 = testValue1;
        }

        public int testValue0;

        [SerializeField]
        private List<float> testValue1;
    }

    void Start()
    {
        PythonConnector.instance.RegisterAction(typeof(TestDataClass), OnDataReceived);

        if (PythonConnector.instance.StartConnection())
        {
            Debug.Log("Connected");
        }
        else
        {
            Debug.Log("Connection Failed");
        }
    }

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            PythonConnector.instance.StopConnection();
            Debug.Log("Stop");
        }
    }

    public void OnTimeout()
    {
        Debug.Log("Timeout");
    }

    public void OnStop()
    {
        Debug.Log("Stopped");
    }

    public void OnDataReceived(DataClass data)
    {
        TestDataClass testData = data as TestDataClass;

        Debug.Log("testValue0: " + testData.testValue0);
        foreach (float v in testData.v1)
        {
            Debug.Log("testValue1: " + v);
        }

        int v1 = UnityEngine.Random.Range(0, 100);
        List<float> v2 = new List<float>()
        {
            UnityEngine.Random.Range(0.1f, 0.9f),
            UnityEngine.Random.Range(0.1f, 0.9f)
        };
        SendingData sendingData = new SendingData(v1, v2);

        Debug.Log("Sending Data: " + v1 + ", " + v2[0] + ", " + v2[1]);

        PythonConnector.instance.Send("test", sendingData);
    }
}
