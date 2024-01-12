using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using UnityEngine.Events;

abstract class DataDecoder : ScriptableObject
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
