using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using UnityEngine.Events;

abstract class DataDecoder : MonoBehaviour
{
    /// <summary>
    /// Dictionary of data type name to actual C# class type reference
    /// </summary>
    private Dictionary<Type, UnityEvent<DataClass>> correspondingEvents;

    /// <summary>
    /// Convert from data_type name to actual C# class type reference
    /// </summary>
    /// template:
    /// return new Dictionary<string, Type>(){
    ///     {"data_type_name", typeof(C#_class_type)}
    /// }
    public abstract Dictionary<string, Type> DataToType();

    //constructor
    public DataDecoder()
    {
        //get pre-defined data type
        Dictionary<string, Type> dataToType = DataToType();

        //initialize `correspondingEvents`
        PrepareEvents(dataToType.Values.ToArray());
    }

    public void DecodeAndReport(string dataTypeName, string dataJson)
    {
        //get data type
        Type dataType = DataToType()[dataTypeName];

        //convert json to data class
        DataClass data = JsonUtility.FromJson(dataJson, dataType) as DataClass;

        //report data
        correspondingEvents[dataType].Invoke(data);
    }

    /// <summary>
    /// Register new callback when data received
    /// </summary>
    /// <param name="dataType">type of the data class</param>
    /// <param name="callback">callback when data received</param>
    public void RegisterAction(Type dataType, UnityAction<DataClass> callback)
    {
        correspondingEvents[dataType].AddListener(callback);
    }

    /// <summary>
    /// Unregister callback when data received
    /// </summary>
    /// <param name="dataType">type of the data class</param>
    /// <param name="callback">callback when data received</param>
    public void RemoveAction(Type dataType, UnityAction<DataClass> callback)
    {
        correspondingEvents[dataType].RemoveListener(callback);
    }

    private void PrepareEvents(Type[] types)
    {
        //prepare events
        correspondingEvents = new Dictionary<Type, UnityEvent<DataClass>>();
        foreach (Type type in types)
        {
            correspondingEvents.Add(type, new UnityEvent<DataClass>());
        }
    }
}
