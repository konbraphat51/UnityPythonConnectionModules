using System;
using System.Collections.Generic;
using PythonConnection;
using UnityEngine;

[Serializable]
public class TestDataClass : DataClass
{
    public int testValue0;

    [SerializeField]
    private List<float> testValue1;
}
